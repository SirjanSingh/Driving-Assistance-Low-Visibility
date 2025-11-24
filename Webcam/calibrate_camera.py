import cv2
import numpy as np
import glob
import os
import sys

# -------- CONFIG --------
CHECKERBOARD = (6, 6)       # inner corners for your 9x7 squares checkerboard
square_size = 0.025         # meters (25mm) — change if your squares are a different size

# -------- LOAD IMAGES --------
IMAGE_DIR = "images"        # folder where your images are stored

# Load all formats
images = []
for ext in ["png", "jpg", "jpeg", "PNG", "JPG"]:
    images.extend(glob.glob(os.path.join(IMAGE_DIR, f"*.{ext}")))

print("\nFound images:", len(images))

if len(images) == 0:
    print("❌ ERROR: No images found in 'images/' folder.")
    print("Make sure your structure is: Webcam/images/*.png")
    sys.exit()

# -------- PREPARE OBJECT POINTS --------
objp = np.zeros((CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[
    0:CHECKERBOARD[0],
    0:CHECKERBOARD[1]
].T.reshape(-1, 2)

objp *= square_size

objpoints = []   # 3D points
imgpoints = []   # 2D points


# -------- PROCESS EACH IMAGE --------

for fname in images:
    print("Processing:", fname)

    img = cv2.imread(fname)
    if img is None:
        print("⚠️  Could not read image, skipping:", fname)
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    print("  Checkerboard detected =", ret)

    if ret:
        # refine
        corners2 = cv2.cornerSubPix(
            gray,
            corners,
            (11, 11),
            (-1, -1),
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        )

        objpoints.append(objp)
        imgpoints.append(corners2)

        # show preview
        cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
        cv2.imshow("Detection", img)
        cv2.waitKey(200)

cv2.destroyAllWindows()

print("\nValid detected images:", len(imgpoints))

if len(imgpoints) < 10:
    print("❌ ERROR: Not enough good images (need at least 10).")
    sys.exit()

# -------- CALIBRATE CAMERA --------
print("\nRunning calibration...")

ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("\n=========== CALIBRATION COMPLETE ===========")
print("Camera Matrix:\n", camera_matrix)
print("Distortion Coefficients:\n", dist_coeffs)
print("RMS Reprojection Error:", ret)

# -------- SAVE RESULTS --------
np.save("camera_matrix.npy", camera_matrix)
np.save("dist_coeffs.npy", dist_coeffs)

print("\nSaved → camera_matrix.npy")
print("Saved → dist_coeffs.npy")
