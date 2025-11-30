from ultralytics import YOLO

model = YOLO("yolo12s.pt")

results = model.train(
    data="dataset2/data.yaml",
    epochs=200,
    imgsz=640,
    batch=16,
    device=0,
    workers=8,
    name="yolov12_driving_assist2",
    project="runs/train",
    patience=20,
    exist_ok=True
)

print("Training complete! Best weights saved in:", results.save_dir)




