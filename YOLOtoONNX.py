from ultralytics import YOLO

model = YOLO("spf_v3.pt")
model.export(format="onnx")