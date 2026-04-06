
# !pip install roboflow

# from roboflow import Roboflow
# rf = Roboflow(api_key="bPpdujFfoLfYGtndsJuI")
# project = rf.workspace("fist-le8b1").project("red-kfs")
# version = project.version(5)
# dataset = version.download("yolo26")
                      
                

from ultralytics import YOLO

def main():
    model = YOLO("yolo26n.pt")  # or your custom pretrained model
    model.train(
        data=r"C:\Users\SIDDHARTH\Downloads\opencv\Red-KFS-5\data.yaml",
        epochs=150,
        imgsz=640,
        batch=16,
        workers=4   # can adjust later
    )

if __name__ == "__main__":
    main()
