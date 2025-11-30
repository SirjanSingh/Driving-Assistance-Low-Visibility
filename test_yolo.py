from ultralytics import YOLO

model = YOLO("runs/train/yolov12_driving_assist2/weights/best.pt")

results = model.val(
    data="dataset2/data.yaml",
    split='test',
    name="yolov12_test_results",
    project="runs/test",
    save=True,       
    save_txt=True,   
    save_json=True
)

print("✅ Test complete! Results saved in:", results.save_dir)

