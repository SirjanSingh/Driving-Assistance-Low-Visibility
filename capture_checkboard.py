import cv2
import os
import time
import csv
from datetime import datetime
import numpy as np

# ---------- CONFIG ----------
CAM_INDEX = 0                 # Logitech C922
BACKEND = cv2.CAP_DSHOW       # Windows backend
OUT_DIR = "images"
LOG_CSV = os.path.join(OUT_DIR, "capture_log.csv")

# CORRECT FOR YOUR PRINTED 9x7 SQUARE CHECKERBOARD
CHECKERBOARD = (6, 6)         # inner corners

AUTO_SAVE = True              
AUTO_SAVE_AREA_RATIO = 0.18   
MIN_SECONDS_BETWEEN_SAVES = 1.0
MAX_IMAGES = 60               

# ---------- SETUP ----------
os.makedirs(OUT_DIR, exist_ok=True)

# Create log file if missing
if not os.path.exists(LOG_CSV):
    with open(LOG_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "timestamp", "method", "frame_width", "frame_height"])

cap = cv2.VideoCapture(CAM_INDEX, BACKEND)
if not cap.isOpened():
    print(f"❌ Could not open camera at index {CAM_INDEX}")
    exit()

print("✅ Camera opened. Controls: SPACE=manual save, a=toggle auto-save, q=quit")

last_save_time = 0
saved_count = len([n for n in os.listdir(OUT_DIR) if n.lower().endswith(('.png','.jpg'))])
last_center = None

# Termination criteria for corner refinement
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to read frame")
        break

    h, w = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # DETECT 8x6 INNER CORNERS
    found, corners = cv2.findChessboardCorners(
        gray,
        CHECKERBOARD,
        cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE
    )

    display = frame.copy()

    if found:
        # refine accuracy
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        cv2.drawChessboardCorners(display, CHECKERBOARD, corners2, found)

        pts = corners2.reshape(-1,2)
        x_min, y_min = pts.min(axis=0).astype(int)
        x_max, y_max = pts.max(axis=0).astype(int)
        bbox_area = (x_max - x_min) * (y_max - y_min)
        area_ratio = bbox_area / (h*w)

        # movement detection center
        cx = int((x_min + x_max)/2)
        cy = int((y_min + y_max)/2)
        cur_center = (cx, cy)

        # Draw bounding box
        cv2.rectangle(display, (x_min, y_min), (x_max, y_max), (0,255,0), 2)
        cv2.putText(display, "Corners detected", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

        # auto-save logic
        time_ok = (time.time() - last_save_time) >= MIN_SECONDS_BETWEEN_SAVES
        moved_ok = True
        if last_center is not None:
            dx = cur_center[0] - last_center[0]
            dy = cur_center[1] - last_center[1]
            moved_ok = (dx*dx + dy*dy) > (20*20)

        if AUTO_SAVE and area_ratio >= AUTO_SAVE_AREA_RATIO and time_ok and moved_ok:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            fname = f"checker_{saved_count:03d}_{timestamp}.png"
            path = os.path.join(OUT_DIR, fname)
            cv2.imwrite(path, frame)

            with open(LOG_CSV, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([fname, timestamp, "auto", w, h])

            print("Auto-saved:", fname)
            saved_count += 1
            last_save_time = time.time()

        last_center = cur_center

    else:
        cv2.putText(display, "Checkerboard NOT detected", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

    # status
    cv2.putText(display, f"Saved: {saved_count}", (10,h-20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

    cv2.imshow("Checkerboard Capture", display)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord(' '):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"checker_{saved_count:03d}_{timestamp}.png"
        path = os.path.join(OUT_DIR, fname)
        cv2.imwrite(path, frame)
        print("Manual saved:", fname)
        saved_count += 1
    if key == ord('a'):
        AUTO_SAVE = not AUTO_SAVE
        print("AUTO_SAVE:", AUTO_SAVE)

cap.release()
cv2.destroyAllWindows()
print("Done. Images saved in:", OUT_DIR)
