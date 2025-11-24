import cv2

# Open Logitech C922 at index 1 using DirectShow backend
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("❌ Could not open camera at index 1")
    exit()

print("✅ Camera 1 opened successfully! Press Q to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to read frame")
        break

    cv2.imshow("Logitech C922 (Index 1)", frame)

    # Quit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
