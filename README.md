# 🚗 DriveGuard AI
### *Low-Visibility Driving Assistance System (Edge AI + YOLOv12s + Raspberry Pi)*

## 🔍 Overview
DriveGuard AI is a real-time **on-edge driving assistance system** designed to help detect hazards in **fog, rain, night, and low-visibility environments**.

The system:
- Detects **cars, people, bikes, dogs, potholes**
- Runs **fully offline**
- Deploys on a **Raspberry Pi**
- Uses a **YOLOv12-s model optimized through Edge Impulse**
- Estimates distance using calibrated camera geometry and issues alerts

---

## 🧠 AI Workflow Summary

### 1️⃣ Dataset Preparation
- Collected fog/low-visibility road images
- Annotated dataset in **YOLO format**
- Classes:

```
Car
Dog
Motorbike
People
Pothole
```

---

### 2️⃣ YOLOv12-s Model Training (Locally)

Command used:
```
yolo train model=yolov12s.pt data=data.yaml imgsz=640 epochs=100
```

Exported for Edge Impulse:
```
yolo export model=best.pt format=onnx opset=12 simplify=True
```

---

### 3️⃣ Edge Impulse Optimization & Deployment Conversion

Steps performed in Edge Impulse:

| Step | Status |
|------|--------|
| Created Project | ✔ |
| Uploaded dataset (images + labels) | ✔ |
| Added label map file | ✔ |
| Uploaded ONNX YOLO model | ✔ |
| Automatically validated model shape | ✔ |
| Generated ARM-ready `.eim` runtime bundle | ✔ |

Edge Impulse handled:
- Model quantization  
- Input/Output reshaping  
- ARM runtime packaging  
- Real-time deployment preview  

---

### 4️⃣ Raspberry Pi Deployment

Downloaded generated model file:

```
sirjansingh-project-1-linux-armv7.eim
```

Installed runtime on Raspberry Pi:

```
pip install edge_impulse_linux
```

Run model with camera:

```
edge-impulse-linux-runner --model-file sirjansingh-project-1-linux-armv7.eim
```

Output:

- Displays bounding boxes in real-time  
- Provides web dashboard at:  
  👉 `http://<raspberry-pi-ip>:4912`

---

## 📏 Distance Estimation Formula

```
pixel_angle = atan((y - cy) / fy)
angle = camera_tilt + pixel_angle
distance = camera_height / tan(angle)
```

Used for hazard scoring and emergency alerts.

---

## 🧪 Performance Summary

| Metric | Result |
|--------|--------|
| Raspberry Pi Runtime | ~10–20 FPS |
| Laptop Runtime | ~30–60 FPS |
| Requires Internet? | ❌ No (fully offline) |
| Model Format | `.onnx` → `.eim` optimized |
| Accuracy improves in fog/night scenarios | ✔ |

---

## 🛠 Run the System

Laptop (raw YOLO inference):

```
python detect_video.py
```

Raspberry Pi (Edge Impulse optimized):

```
edge-impulse-linux-runner --model-file *.eim
```

---

## 🎯 Key Features

- Fast on-device inference  
- Works in low visibility  
- Fully offline system  
- Distance + hazard alerts  
- Raspberry Pi compatible  

---

## 🚀 Future Improvements

- Lane detection  
- Speed tracking (SORT/DeepSORT)  
- LiDAR + Camera fusion  
- IR/thermal night mode  

---

## 👤 Author
**Ritigya Gupta**, 
**Sirjan Singh**, 
**Heeral Mandolia**

---

### Status: Prototype Complete ✔
