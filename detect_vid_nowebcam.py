from ultralytics import YOLO
import cv2
import numpy as np
import math
import winsound
import time
import torch
import os

# CAMERA CALIBRATION PARAMETERS

fx = 1030.12416
fy = 1026.17047
cx = 327.044214
cy = 107.086996

H = 0.27   # camera height (meters)
theta_deg = 12
theta = math.radians(theta_deg)

def estimate_distance(y_pixel):
    v = cy
    delta_y = fy
    numerator = H * math.cos(theta)
    denominator = math.sin(theta) + ((v - y_pixel) / delta_y) * math.cos(theta)
    Z = numerator / denominator
    return max(Z, 0.05)

# LOAD YOLO 
device = "cuda" if torch.cuda.is_available() else "cpu"
print("🔥 Using Device:", device.upper())

model = YOLO("runs/train/yolov12_driving_assist2/weights/best.pt")
model.to(device)

# VIDEO INPUT FILE
video_path = "videos/Video_Generation_With_Added_People.mp4"     
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("❌ Could not open video file!")
    exit()

# Drop frame buffering → zero lag
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

out = cv2.VideoWriter(
    "annotated_output.mp4",
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (width, height)
)

previous_alert = ""
last_beep_time = 0  # stop too many beeps

print("✔ Processing video...")

# --------------------------------------
# MAIN PROCESSING LOOP
# --------------------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        print("✔ Finished processing video.")
        break

    # Faster inference by reducing size → huge FPS improvement
    results = model(frame, imgsz=416, verbose=False, device=device)

    annotated = frame.copy()
    classes_detected = []

    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        cls = int(box.cls[0])
        class_name = model.names[cls]
        classes_detected.append(class_name)

        # Distance
        distance = estimate_distance(y2)

        # Confidence
        conf = float(box.conf[0])

        cv2.rectangle(annotated, (int(x1), int(y1)),
                      (int(x2), int(y2)), (0, 255, 0), 2)

        label = f"{class_name} {distance:.2f} m ({conf*100:.1f}%)"
        cv2.putText(annotated, label, (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # --------------------------------------
    # ALERT + SUPER FAST BEEP (NO LAG)
    # --------------------------------------
    unique_classes = sorted(set(classes_detected))

    if unique_classes:
        alert_text = " and ".join(unique_classes)
        message = f"Warning! {alert_text} ahead."

        # Beep only when message changes AND minimum 0.4 sec between beeps
        if message != previous_alert and time.time() - last_beep_time > 0.4:
            winsound.Beep(1000, 80)   # Faster & non-blocking
            last_beep_time = time.time()
            previous_alert = message

        cv2.putText(annotated, message, (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # --------------------------------------
    # DISPLAY AND SAVE
    # --------------------------------------
    out.write(annotated)
    cv2.imshow("Video Detection", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

print("✔ Output saved as annotated_output.mp4")
