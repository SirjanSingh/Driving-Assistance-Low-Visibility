# DriveGuard AI – Low-Visibility Driving Assistance System  
### *Edge AI • YOLOv12-s • Raspberry Pi • Real-Time Distance Estimation*

![banner](images/banner.jpg)
*(Replace with your banner image inside /images)*

---

## Overview  
DriveGuard AI is an **Edge-powered intelligent driving assistance system** built for **fog, night, rain, dust, and low-visibility scenarios**.  
It performs **real-time object detection, distance estimation, and safety alerts** using:

* **YOLOv12-s** (custom trained)
* **Edge Impulse** optimized quantized model
* **Raspberry Pi** deployment
* Full **camera calibration** ($f_x, f_y, c_x, c_y$, height, tilt)

Runs fully **offline** on edge devices $\rightarrow$ ideal for on-road safety.

---

# 📸 Screenshots  

### Detection Examples  
![detection1](images/detection1.jpg)  
![detection2](images/detection2.jpg)

### Alerts + Distance Overlay  
![alerts](images/alerts.jpg)

---

# Key Features  

## Core AI Capabilities  
* **YOLOv12-s** optimized for fog & low-light  
* Multi-object detection: cars, pedestrians, animals  
* Fast inference on laptop + Raspberry Pi  
* Edge Impulse quantized acceleration  

## 📏 Advanced Intelligence  
* **Real-time calibrated distance estimation** $\leftarrow$ Crucial for safety!
* **Pinhole camera geometry** + tilt correction  
* Multi-object threat detection  
* On-screen bounding boxes + distance overlay  

## Safety Alerts  
* Windows $\rightarrow$ winsound beep  
* Raspberry Pi $\rightarrow$ **GPIO buzzer alerts**  
* Warnings only when objects enter danger zone  

## Edge Deployment  
* Raspberry Pi 4 / 5 support  
* Raspberry Pi Camera Module v3 ready  
* $<100\text{ms}$ inference using `.eim` model  

---

# Architecture  

![architecture](images/architecture.png)  
*(Add your architecture diagram here)*

---

# Quick Start  

## Requirements  
* Python 3.8+  
* Raspberry Pi (optional)  
* USB Webcam or Pi Camera v3  
* Edge Impulse account  
* YOLOv12-s weights (`yolov12s.pt`)

---

## ⚙️ Installation  

### 1. Clone repository  
```bash
git clone [https://github.com/yourusername/Driving-Assistance-AI](https://github.com/yourusername/Driving-Assistance-AI)
cd Driving-Assistance-AI
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/Scripts/activate   # Windows
source venv/bin/activate       # Linux / Raspberry Pi
```

### 3. Install dependencies
```bash
pip install ultralytics opencv-python numpy
```

### 4. Add YOLO model
Place model file here:

/models/yolov12s.pt

### Run the System
On Laptop
```bash
python detect_video.py
```
On Raspberry Pi
```bash
python detect_video_pi.py
```

### Expected Console Output
```bash
Opening webcam at index 0...
✔ Webcam opened successfully!
ALERT: Warning! Car ahead. Distance: 4.2m
```

Model Training (Edge Impulse)
Steps

Create a new project on Edge Impulse

Upload dataset (fog, night, rain, low-light)

Select Image → Object Detection

Train YOLO-compatible model

Export as:

YOLO format (Python inference)

.eim format (Raspberry Pi optimized)

Full guide:

/docs/EDGE_IMPULSE_GUIDE.md

### Distance Estimation Formula
```bash
pixel_angle = atan((y_pixel - cy) / fy)
total_angle = camera_tilt_angle + pixel_angle
distance_Z = H / tan(total_angle)
```

### Performance
```bash
Metric                    Result
--------------------------------------------
FPS (Laptop)              30–60 FPS
FPS (Raspberry Pi 4)      10–20 FPS
Distance Accuracy         ±5–10% after calibration
Model Size                ~20MB
Detection Targets         Cars, Pedestrians, Animals, Hazards

```
### Innovation

Works in fog, night & extreme low visibility

Hybrid YOLO + geometric distance system

Fully offline Edge AI with Raspberry Pi

Complete camera calibration pipeline

Real-time multi-object hazard alerts

Edge Impulse model compression → high FPS
