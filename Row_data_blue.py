def first_row(left_class, mid_class, right_class, box_dict,data_to_next,  class_of_next):
        box_dict[3] = right_class
        box_dict[2] = mid_class
        box_dict[1] = left_class

        for i in box_dict:
            if box_dict[i]=='R2Real':
                data_to_next = i
                class_of_next[0] = box_dict[i]
                break
        return box_dict, data_to_next, class_of_next


def further_rows(left_class, mid_class, right_class, curr_pos, curr_row, curr_column, box_dict, class_of_next, data_to_next, pos_to_change, next_pos):
        if curr_pos[0] in [1, 2, 3]:
            curr_row[0] = 1
            if curr_column[0]==1:
                box_dict[4] = mid_class
                box_dict[5] = right_class
                class_of_next[0] = box_dict[4]
                if class_of_next[0] in ['R2Real', 'empty']:
                    data_to_next=4
                    next_pos[0] = 4
                    pos_to_change = True
                    class_of_next[0] = box_dict[4]

                elif class_of_next[0] in ['Rsymbol', 'Fake']:
                     data_to_next =2
                     next_pos[0] = 2
                     pos_to_change = False
                     class_of_next[0] = box_dict[2]
            elif  curr_column[0]==2:
                box_dict[4] = left_class
                box_dict[5] = mid_class
                box_dict[6] = right_class
                class_of_next[0] = box_dict[5]
                if class_of_next[0] in ['R2Real' , 'empty']:
                     data_to_next=5
                     next_pos[0] = 5
                     pos_to_change = True
                     class_of_next[0] = box_dict[5]
                elif class_of_next[0] in ['Rsymbol' , 'Fake']:
                     data_to_next = 1
                     next_pos[0] = 1
                     pos_to_change= False
                     class_of_next[0] = box_dict[1]

            elif curr_column[0]==3:
                box_dict[6] = mid_class
                box_dict[5] = left_class
                class_of_next[0] = box_dict[6]
                if class_of_next[0] in ['R2Real' , 'empty']:
                    data_to_next=6
                    next_pos[0] = 6
                    pos_to_change=True
                    class_of_next[0] = box_dict[6]

                elif class_of_next[0] in ['Rsymbol' , 'Fake']:
                     data_to_next =2
                     next_pos[0] = 2
                     pos_to_change=False
                     class_of_next[0] = box_dict[2]
        elif curr_pos[0] in [4 , 5 , 6]:
            curr_row[0] = 2
            if curr_column[0]==1:
                box_dict[7] = mid_class
                box_dict[8] = right_class
                class_of_next[0] = box_dict[7]
                if class_of_next[0] in ['R2Real' , 'empty']:
                    data_to_next=7
                    next_pos[0] = 7
                    pos_to_change=True
                    class_of_next[0] = box_dict[7]

                elif class_of_next[0] in ['Rsymbol' , 'Fake']:
                     data_to_next =5
                     next_pos[0] = 5
                     pos_to_change=False
                     class_of_next[0] = box_dict[5]
            elif  curr_column[0]==2:
                box_dict[7] = left_class
                box_dict[8] = mid_class
                box_dict[9] = right_class
                class_of_next[0] = box_dict[8]
                if class_of_next[0] in ['R2Real' , 'empty']:
                     data_to_next = 8
                     next_pos[0] = 8
                     pos_to_change = True
                     class_of_next[0] = box_dict[8]
                elif class_of_next[0] in ['Rsymbol' , 'Fake']:
                     data_to_next = 4
                     next_pos[0] = 4
                     pos_to_change = False
                     class_of_next[0] = box_dict[4]
            elif curr_column[0]==3:
                box_dict[9] = mid_class
                box_dict[8] = left_class
                class_of_next[0] = box_dict[9]
                if class_of_next[0] in ['R2Real' , 'empty']:
                    data_to_next=9
                    next_pos[0] = 9
                    pos_to_change = True
                    class_of_next[0] = box_dict[9]

                elif class_of_next[0] in ['Rsymbol' , 'Fake']:
                     data_to_next =5
                     next_pos[0] = 5
                     pos_to_change = False  
                     class_of_next[0] = box_dict[5]
        elif curr_pos[0] in [7 , 8 , 9]:
            curr_row[0] = 3
            if curr_column[0]==1:
                box_dict[10] = mid_class
                box_dict[11] = right_class
                class_of_next[0] = box_dict[10]
                if class_of_next[0] in ['R2Real' , 'empty']:
                    data_to_next=10
                    next_pos[0] = 10
                    pos_to_change = True
                    class_of_next[0] = box_dict[10]

                elif class_of_next[0] in ['Rsymbol' , 'Fake']:
                     data_to_next =8
                     next_pos[0] = 8
                     pos_to_change=False
                     class_of_next[0] = box_dict[8]
            elif  curr_column[0]==2:
                box_dict[10] = left_class
                box_dict[11] = mid_class
                box_dict[12] = right_class
                class_of_next[0] = box_dict[11]
                if class_of_next[0] in ['R2Real' , 'empty']:
                     data_to_next = 11
                     next_pos[0] = 11
                     pos_to_change = True
                     class_of_next[0] = box_dict[11]
                elif class_of_next[0] in ['Rsymbol' , 'Fake']:
                     data_to_next = 7
                     next_pos[0] = 7
                     pos_to_change = False
                     class_of_next[0] = box_dict[7]
            elif curr_column[0]==3:
                box_dict[12] = mid_class
                box_dict[11] = left_class
                class_of_next[0] = box_dict[12]
                if class_of_next[0] in ['R2Real' , 'empty']:
                    data_to_next=12
                    next_pos[0] = 12
                    pos_to_change = True
                    class_of_next[0] = box_dict[12]

                elif class_of_next[0] in ['Rsymbol' , 'Fake']:
                     data_to_next =8
                     next_pos[0] = 8
                     pos_to_change = False
                     class_of_next[0] = box_dict[8]
        elif curr_pos[0] in [10 , 11 , 12]:
                curr_row[0] = 4
                class_of_next[0] = 'exit'
                next_pos[0] = 'exit'
                pos_to_change = pos_to_change
                class_of_next[0] = 'exit'
        return curr_row, curr_column, box_dict, class_of_next, data_to_next, pos_to_change, next_pos, curr_pos