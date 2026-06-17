from ultralytics import YOLO
model=YOLO("symbol300.pt")
results=model(source=0,show=True,conf=0.7,save=True)