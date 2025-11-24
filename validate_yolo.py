from ultralytics import YOLO

model = YOLO("runs/train/yolov12_driving_assist2/weights/best.pt")

results = model.val(data="dataset2/data.yaml")

