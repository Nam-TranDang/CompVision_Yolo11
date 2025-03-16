# from ultralytics import YOLO

# # Load the model
# model = YOLO("yolo11n.pt")

# # Train the model
# results = model.train(
#     data="dataset.yaml",
#     epochs=50,
#     imgsz=640,
#     batch=8,  # Adjust if VRAM is insufficient
#     device=0  # Use GPU
#     resume=True
# )

# from ultralytics import YOLO

# if __name__ == '__main__':
#     model = YOLO("yolo11n.pt")
#     results = model.train(
#         data="dataset.yaml",
#         epochs=10,
#         imgsz=640,
#         batch=8,
#         device=0
#     )
from ultralytics import YOLO

if __name__ == "__main__":
    # Load a model
    model = YOLO("yolo11n.pt")  # Load pretrained model

    # Train the model
    results = model.train(data="dataset.yaml", epochs=100, imgsz=640, batch=8, workers=4)
    #device = 0