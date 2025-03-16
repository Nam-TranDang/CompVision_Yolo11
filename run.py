from ultralytics import YOLO

model = YOLO("yolo11n.pt") 

result = model("F:\yolo_11\Leeds.mp4", save=True, show=True, device=0)