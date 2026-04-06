# left_detect.py
def process_left(results,frame, model):
    pos1 = "Empty"
    left_class="Empty"

    for result in results:
        frame = result.plot()
        for box in result.boxes:
            xl1, yl1, xl2, yl2 = map(int, box.xyxy[0])
            xlc = (xl1 + xl2) // 2
            ylc = (yl1 + yl2) // 2

            cls_id = int(box.cls[0])
            class_name = model.names[cls_id]
            
            if 0 <= xlc <= 320 and 160 <= ylc <= 320:
                left_class=class_name
            elif 320 <= xlc <= 640 and 160 <= ylc <= 320:
                pos1=class_name
                
        
        

    return left_class, pos1
