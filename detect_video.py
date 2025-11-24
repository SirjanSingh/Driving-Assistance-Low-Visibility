from ultralytics import YOLO
import cv2
import numpy as np
import math
import winsound   # ✔ built-in sound player for WAV
import os

# --------------------------------------
# CAMERA CALIBRATION PARAMETERS
# --------------------------------------
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

# --------------------------------------
# LOAD YOLO MODEL
# --------------------------------------
model = YOLO("runs/train/yolov12_driving_assist2/weights/best.pt")

# --------------------------------------
# WEBCAM SETUP
# --------------------------------------
print("Opening webcam at index 0...")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("❌ Could not open webcam at index 0, trying index 1...")
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("❌ Could not open ANY webcam.")
    exit()

print("✔ Webcam opened successfully!")

# Set resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

fps = 30
annotated_video = "webcam_annotated.mp4"

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(annotated_video, fourcc, fps, (640, 480))

previous_alert = ""

print("✔ Webcam running. Press Q to quit.")

# --------------------------------------
# WEBCAM LOOP
# --------------------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Webcam stopped sending frames.")
        break

    results = model(frame, verbose=False)
    annotated = frame.copy()

    classes_detected = []

    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        cls = int(box.cls[0])
        class_name = model.names[cls]

        classes_detected.append(class_name)

        # Distance estimation
        y_bottom = y2
        distance = estimate_distance(y_bottom)

        # Confidence score
        conf = float(box.conf[0])

        cv2.rectangle(annotated, (int(x1), int(y1)),
                      (int(x2), int(y2)), (0, 255, 0), 2)

        label = f"{class_name} {distance:.2f} m ({conf*100:.1f}%)"
        cv2.putText(annotated, label, (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # ------- ALERT SYSTEM WITH BEEP SOUND -------
    unique_classes = sorted(set(classes_detected))

    if unique_classes:
        alert_text = " and ".join(unique_classes)
        message = f"Warning! {alert_text} ahead."

        if message != previous_alert:
            print("🔔 ALERT:", message)

            # 🔊 play your beep.wav (non-blocking)
            winsound.PlaySound("beep.wav",
                               winsound.SND_FILENAME | winsound.SND_ASYNC)

            previous_alert = message

        cv2.putText(annotated, message, (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # --------------------------------------
    # DISPLAY + SAVE VIDEO
    # --------------------------------------
    out.write(annotated)
    cv2.imshow("Webcam Detection", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

print("✔ Saved webcam_annotated.mp4")
print("✔ Program finished.")
