from zone2_leftDetect import process_left as ld
from zone2_rightDetect import process_right as rd
from zone2_centerDetect import process_center as cd

def path(scroll_dict_empty, curr_position, curr_column, curr_row,right_class, center_class, left_class, class_of_next):

    
    if curr_position == [0, 0]:

        
        for i in scroll_dict_empty:

            if scroll_dict_empty[i] == "R2Real" and (i==1 or i==2 or i==3):
                
                curr_position[0] = i
                curr_position[1]=1
                curr_column = i
                class_of_next = "R2Real"
                data_to_next=i
                
                break   

    elif curr_position[0] == 1:
        scroll_dict_empty[5] = left_class
        scroll_dict_empty[4] = center_class
        print("Current Position: ",curr_position[0])
        if scroll_dict_empty[4] in ("Rsymbol", "Fake"):
            curr_position[0]=2
            curr_position[1]=1
            class_of_next = scroll_dict_empty[4]
            curr_column=2
            data_to_next=2
        elif scroll_dict_empty[4]in ("R2Real", "Empty"):
            curr_position[0]=4
            curr_position[1]=2
            curr_column=1
            curr_row=2
            class_of_next=scroll_dict_empty[4]
            data_to_next=4
    
    elif curr_position[0]==2:
        scroll_dict_empty[4]=right_class
        scroll_dict_empty[5]=center_class
        scroll_dict_empty[6]=left_class
        print("Current Position: ",curr_position[0])
        if scroll_dict_empty[5] in ("Rsymbol", "Fake"):
            curr_position[0]=1
            curr_position[1]=1
            curr_column=1
            data_to_next=1
            class_of_next = scroll_dict_empty[5]
        elif scroll_dict_empty[5] in ("R2Real", "Empty"):
            curr_position[0]=5
            curr_position[1]=2
            curr_column=2
            curr_row=2
            class_of_next=scroll_dict_empty[5]
            data_to_next=5
    
    elif curr_position[0]==3:
        scroll_dict_empty[6]=center_class
        scroll_dict_empty[5]=right_class
        print("Current Position: ",curr_position[0])
        if scroll_dict_empty[6] in ("Rsymbol", "Fake"):
            curr_position[0]=2
            curr_position[1]=1
            curr_column=2
            class_of_next = scroll_dict_empty[6]
            data_to_next=2
        elif scroll_dict_empty[6]in ("R2Real", "Empty"):
            curr_position[0]=6
            curr_position[1]=2
            curr_column=1
            curr_row=2
            class_of_next=scroll_dict_empty[6]
            data_to_next=6
    
    elif curr_position[0] == 4:
        scroll_dict_empty[8] = left_class
        scroll_dict_empty[7] = center_class
        print("Current Position: ",curr_position[0])
        if scroll_dict_empty[7] in ("Rsymbol", "Fake"):
            curr_position[0] = 5
            curr_position[1]=2
            curr_column = 2
            data_to_next = 5
            class_of_next = scroll_dict_empty[7]

        elif scroll_dict_empty[7] in ("R2Real", "Empty"):
            curr_position[0] = 7
            curr_position[1]=3
            curr_column = 1
            curr_row = 3
            class_of_next = scroll_dict_empty[7]
            data_to_next = 7
    
    elif curr_position[0] == 5:
        scroll_dict_empty[7] = left_class
        scroll_dict_empty[8] = center_class
        scroll_dict_empty[9] = right_class
        print("Current Position: ",curr_position[0])
        if scroll_dict_empty[8] in ("Rsymbol", "Fake"):
            curr_position[0] = 4
            curr_position[1]=2
            curr_column = 1
            data_to_next = 4
            class_of_next = scroll_dict_empty[8]

        elif scroll_dict_empty[8] in ("R2Real", "Empty"):
            curr_position[0] = 8
            curr_position[1]=3
            curr_column = 2
            curr_row = 3
            class_of_next = scroll_dict_empty[8]
            data_to_next = 8

    elif curr_position[0] == 6:
        scroll_dict_empty[9]=center_class
        scroll_dict_empty[8]=right_class   
        print("Current Position: ",curr_position[0])
        if scroll_dict_empty[9] in ("Rsymbol", "Fake"):
            curr_position[0] = 5
            curr_position[1]=2
            curr_column = 2
            data_to_next = 5
            class_of_next = scroll_dict_empty[9]

        elif scroll_dict_empty[9] in ("R2Real", "Empty"):
            curr_position[0] = 9
            curr_position[1]=3
            curr_column = 3
            curr_row = 3
            class_of_next = scroll_dict_empty[9]
            data_to_next = 9
    
    elif curr_position[0] == 7:
        scroll_dict_empty[11] = left_class
        scroll_dict_empty[10] = center_class
        print("Current Position: ",curr_position[0])
        if scroll_dict_empty[10] in ("Rsymbol", "Fake"):
            curr_position[0] = 8
            curr_position[1]=3
            curr_column = 2
            data_to_next = 8
            class_of_next = scroll_dict_empty[10]
        elif scroll_dict_empty[10] in ("R2Real", "Empty"):
            curr_position[0] = 10
            curr_position[1]=4
            curr_column = 1
            curr_row = 4
            class_of_next = scroll_dict_empty[10]
            data_to_next = 10
    
    elif curr_position[0] == 8:
        scroll_dict_empty[10] = left_class
        scroll_dict_empty[11] = center_class
        scroll_dict_empty[12] = right_class
        print("Current Position: ",curr_position[0])
        if scroll_dict_empty[11] in ("Rsymbol", "Fake"):
            curr_position[0] = 7
            curr_position[1]=3
            curr_column = 1
            data_to_next = 7
            class_of_next = scroll_dict_empty[11]
        elif scroll_dict_empty[11] in ("R2Real", "Empty"):
            curr_position[0] = 11
            curr_position[1]=4
            curr_column = 2
            curr_row = 4
            class_of_next = scroll_dict_empty[11]
            data_to_next = 11
    
    elif curr_position[0] == 9:

        scroll_dict_empty[12]=center_class
        scroll_dict_empty[11]=right_class
        print("Current Position: ",curr_position[0])
        if scroll_dict_empty[12] in ("Rsymbol", "Fake"):
            curr_position[0] = 8
            curr_position[1]=3
            curr_column = 2
            data_to_next = 8
            class_of_next = scroll_dict_empty[12]
        elif scroll_dict_empty[12] in ("R2Real", "Empty"):
            curr_position[0] = 12
            curr_position[1]=4
            curr_column = 3
            curr_row = 4
            class_of_next = scroll_dict_empty[12]
            data_to_next = 12

    elif curr_position[0] == 10:
    
        scroll_dict_empty[10] = right_class
        print("Current Position: ",curr_position[0])
        class_of_next="Exit"
        curr_position[0]='Exit'
        data_to_next='Exit'
        curr_column[0]=1
        # if scroll_dict_empty[10] in ("Rsymbol", "Fake"):
        #     curr_position[0] = 11
        #     curr_position[1]=4
        #     curr_column = 2
        #     data_to_next = 11
        #     class_of_next = scroll_dict_empty[10]
        # else:
        
        #     class_of_next = scroll_dict_empty[10]
        #     data_to_next = "END"

    elif curr_position[0] == 11:
        scroll_dict_empty[11] = center_class
        print("Current Position: ",curr_position[0])
        class_of_next="Exit"
        curr_position[0]='Exit'
        data_to_next='Exit'
        curr_column[0]=1
        # if scroll_dict_empty[11] in ("Rsymbol", "Fake"):
        #     curr_position[0] = 10
        #     curr_position[1]=4
        #     curr_column = 1
        #     data_to_next = 10
        #     class_of_next = scroll_dict_empty[11]
        # else:
        
        #     class_of_next = scroll_dict_empty[11]
        #     data_to_next = "END"

    elif curr_position[0] == 12:
        scroll_dict_empty[12] = left_class
        print("Current Position: ",curr_position[0])
        class_of_next="Exit"
        curr_position[0]='Exit'
        data_to_next='Exit'
        curr_column[0]=1
        # if scroll_dict_empty[12] in ("Rsymbol", "Fake"):
        #     curr_position[0] = 11
        #     curr_position[1]=4
        #     curr_column = 2
        #     data_to_next = 11
        #     class_of_next = scroll_dict_empty[12]
        # else:
        
        #     class_of_next = scroll_dict_empty[12]
        #     data_to_next = "END"


    return curr_position, curr_column, class_of_next,data_to_next
    

        
        # if curr_position[0]==0 and curr_position[1]==0:
        #     for i in scroll_dict_empty:
        #         if scroll_dict_empty[i]=="R2Real" and (i=="1" or i=="2" or i=="3"):
        #             curr_position[0]=int(i)
        #             curr_position[1]=1
        #             curr_column=int(i)
        #             curr_row=1
        #             print(curr_position)
        #             print(curr_row,curr_column)
        #             break
    # if curr_position[0]==1 or curr_position[0]==2 or curr_position[0]==3:
    #     for i in scroll_dict_empty:
    #         if scroll_dict_empty[i]:
    #             pass