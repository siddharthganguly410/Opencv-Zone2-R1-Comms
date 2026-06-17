from ultralytics import YOLO
def Left_camera_Detection(results, model):
    left_class = "empty"
    mid_class = "empty"

    if results[0].boxes is not None:
        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            class_name = model.names[cls_id]

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            xc = (x1 + x2) // 2
            yc = (y1 + y2) // 2

            if 160 < yc < 320:
                if xc < 320:
                    left_class = class_name
                else:
                    mid_class = class_name
    return left_class, mid_class


def Right_camera_Detection(results1, model):
    right_class = "empty"

    if results1[0].boxes is not None:
        for box in results1[0].boxes:
            cls_id = int(box.cls[0])
            class_name = model.names[cls_id]

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            xc1 = (x1 + x2) // 2
            yc1 = (y1 + y2) // 2

            if xc1 >= 320 and 160 < yc1 < 320:
                right_class = class_name

    return right_class