
def process_right(results,frame, model):
    pos2 ="Empty"
    right_class="Empty"

    for result in results:
        frame = result.plot()
        for box in result.boxes:
            xr1, yr1, xr2, yr2 = map(int, box.xyxy[0])
            xrc = (xr1 + xr2) // 2
            yrc = (yr1 + yr2) // 2

            cls_id = int(box.cls[0])
            class_name = model.names[cls_id]
            
            if 320 <= xrc <= 640 and 160 <= yrc <= 320:
                right_class=class_name
            elif 0 <= xrc <= 320 and 160 <= yrc <= 320:
                pos2=class_name
            # center-right region
            # if scroll_dict_empty["1"]!=scroll_list[0]:
            #     if 320 <= xrc <= 640 and 160 <= yrc <= 320 and key == ord('l'):
            #         scroll_dict_empty["1"] = class_name
            #     elif 0 <= xrc <= 320 and 160 <= yrc <= 320:
            #         pos2 = class_name
            #     else :
            #         scroll_dict_empty["1"]=class_name

            # center-left region
            

    return right_class, pos2
