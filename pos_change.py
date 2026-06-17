def pos_is_true(curr_row, curr_column, data_to_next, next_pos, curr_pos, next_column):

    if curr_row[0]==1:
                if curr_column[0]==1:
                    next_pos[0] = data_to_next
                    next_column[0] = curr_column[0]
                    curr_pos[0] = 4
                elif curr_column[0]==2:
                    next_pos[0] = data_to_next
                    next_column[0] = curr_column[0]
                    curr_pos[0] = 5
                elif curr_column[0]==3:
                    next_pos[0] = data_to_next
                    next_column[0] = curr_column[0]
                    curr_pos[0] = 6
    elif curr_row[0]==2:
                if curr_column[0]==1:
                    next_pos[0] = data_to_next
                    next_column[0] = curr_column[0]
                    curr_pos[0] = 7
                elif curr_column[0]==2:
                    next_pos[0] = data_to_next
                    next_column[0] = curr_column[0]
                    curr_pos[0] = 8
                elif curr_column[0]==3:
                    next_pos[0] = data_to_next
                    next_column[0] = curr_column[0]
                    curr_pos[0] = 9
    elif curr_row[0]==3:
                if curr_column[0]==1:
                    next_pos[0] = data_to_next
                    next_column[0] = curr_column[0]
                    curr_pos[0] = 10
                elif curr_column[0]==2:
                    next_pos[0] = data_to_next
                    next_column[0] = curr_column[0]
                    curr_pos[0] = 11
                elif curr_column[0]==3:
                    next_pos[0] = data_to_next
                    next_column[0] = curr_column[0]
                    curr_pos[0] = 12
    elif curr_row[0]==4:
                if curr_column[0]==1:
                    next_pos[0] = data_to_next
                    next_column[0] = curr_column[0]
                elif curr_column[0]==2:
                    next_pos[0] = data_to_next
                    next_column[0] = curr_column[0]
                elif curr_column[0]==3:
                    next_pos[0] = data_to_next
                    next_column[0] = curr_column[0]
    return curr_row, curr_column, data_to_next, next_pos, curr_pos, next_column

def pos_is_false(curr_row, curr_column, data_to_next, next_pos, curr_pos, next_column):
      if curr_row[0]==1:
                if curr_column[0]==1:
                    next_pos[0] = data_to_next
                    next_column[0] = 2
                elif curr_column[0]==2:
                    next_pos[0] = data_to_next
                    next_column[0] = 1
                elif curr_column[0]==3:
                    next_pos[0] = data_to_next
                    next_column[0] = 2
      elif curr_row[0]==2:
                if curr_column[0]==1:
                    next_pos[0] = data_to_next
                    next_column[0] = 2
                elif curr_column[0]==2:
                    next_pos[0] = data_to_next
                    next_column[0] = 1
                elif curr_column[0]==3:
                    next_pos[0] = data_to_next
                    next_column[0] = 2
      elif curr_row[0]==3:
                if curr_column[0]==1:
                    next_pos[0] = data_to_next
                    next_column[0] = 2
                elif curr_column[0]==2:
                    next_pos[0] = data_to_next
                    next_column[0] = 1
                elif curr_column[0]==3:
                    next_pos[0] = data_to_next
                    next_column[0] = 2
      elif curr_row[0]==4:
                if curr_column[0]==1:
                    next_pos[0] = data_to_next
                    next_column[0] = 2
                elif curr_column[0]==2:
                    next_pos[0] = data_to_next
                    next_column[0] = 1
                elif curr_column[0]==3:
                    next_pos[0] = data_to_next
                    next_column[0] = 2
      return curr_row, curr_column, data_to_next, next_pos, curr_pos, next_column