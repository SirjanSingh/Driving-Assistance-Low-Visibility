# Driving Assistance System – Low Visibility Object Detection  
Real-time object detection + distance estimation using **YOLOv12-s**

This project is a driver-assistance system designed to help during **low-visibility conditions** such as fog, nighttime, dust, and heavy rain. It uses **YOLOv12-s** for object detection and a **camera-calibrated distance estimation module** to warn drivers about nearby obstacles in real time.

---

## Features

### Real-time Object Detection  
- Uses **YOLOv12-s**  
- Detects vehicles, pedestrians, animals, etc.  
- Fast inference with optimized processing

### Distance Estimation  
Based on camera calibration parameters and pinhole camera geometry:  
- Focal lengths: fx, fy  
- Principal point: cx, cy  
- Camera height (H)  
- Tilt angle (θ)

Outputs estimated real-world distance (meters).

### Driver Alerts  
- Warns if an object is within a dangerous range  
- Beep alert using Windows `winsound`  
- Example alerts:  
  - "Warning! Car ahead."  
  - "Warning! Dog ahead."  
  - "Warning! Car and Dog ahead."

### Webcam Mode  
- Opens webcam stream  
- Real-time detection and distance overlay  
- Press **Q** to quit  

---

## System Architecture

1. **Frame Capture** – Webcam streaming  
2. **YOLOv12-s Object Detection** – Bounding boxes + class IDs  
3. **Distance Estimation** – Pixel-to-angle mapping → real-world distance  
4. **Alert Module** – Plays beep + prints warnings  
5. **Display Output** – Boxes, labels, distance annotations  



## Installation

### 1️⃣ Create a virtual environment  
```bash
python -m venv venv
source venv/Scripts/activate   # Windows
```

### 2️⃣ Install dependencies  
```bash
pip install ultralytics opencv-python numpy
```

### 3️⃣ Place YOLOv12-s model  
Download or place `yolov12s.pt` inside the **models** folder.

---

## ▶️ Run the Project

```bash
python detect_video.py
```

Expected console output:

```
Opening webcam at index 0...
✔ Webcam opened successfully!
✔ Webcam running. Press Q to quit.
ALERT: Warning! Car ahead.
```

---

## Distance Estimation Formula

```
pixel_angle = atan((y_pixel - cy) / fy)
total_angle = camera_tilt_angle + pixel_angle
distance_Z = H / tan(total_angle)
```

If angle is invalid, distance defaults to a safe value.

---

## Performance Notes
- Lightweight real-time detection  
- Works well on standard webcams  
- Fast YOLOv12-s model ensures minimal delay  

---

## Future Enhancements  
(Not implemented yet)

- Voice alerts  
- Lane detection  
- Better fog/night enhancement  
- GPS integration  
- Mobile app or dashboard

---

## License  
This project is for educational and research use.
b
