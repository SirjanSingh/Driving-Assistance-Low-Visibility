import cv2

print("Testing ALL camera indices...")

for i in range(10):
    print(f"\n=== Trying camera index {i} ===")
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print(f" ❌ Could not open camera {i}")
        continue

    print(f" ✅ Camera {i} opened. Showing feed... (Press q to close this feed)")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow(f"Camera {i}", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
