from collections import Counter
from little_battle import load_config_file
# Don't remove any comments in this file

folder_path = "./invalid_files/"
filepath = folder_path + filepath
# Please create appropriate invalid files in the folder "invalid_files"
# for each unit test according to the comments below and
# then complete them according to the function name

def test_file_not_found(filepath):
  # no need to create a file for FileNotFound
  try:
    f_battle = open(filepath, "r")
  except FileNotFoundError:
    print('FileNotFoundError')
    exit()

#------------------------------------------------------------------------
def test_format_error(filepath):
  # add "format_error_file.txt" in "invalid_files"
  f_battle = open(filepath, "r")
  #Check if there are 5 rows
  try:
    ls = f_battle.readlines()
    if len(ls) != 5:
      raise SyntaxError('Invalid Configuration File: format error!')
    f_battle.close()
  except SyntaxError as se:
    print(se)
    f_battle.close()
    exit()

  #Check if each line is the correct label
  try:
    f_battle = open(filepath, "r")
    check_ls=['Frame:','Water:', 'Wood:', 'Food:', 'Gold:']
    i = 0
    while i<5:
      row = f_battle.readline()
      if i<2:
        label = row[:6]
      else:
        label = row[:5]

      if label != check_ls[i]:
        raise SyntaxError('Invalid Configuration File: format error!')
      i += 1
    f_battle.close()
  except SyntaxError as se:
    print(se)
    f_battle.close()
    exit()

#------------------------------------------------------------------------               
def test_frame_format_error(filepath):
  # add "frame_format_error_file.txt" in "invalid_files"
  f_battle = open(filepath, "r")
  frame = f_battle.readline()

    #Check if there is any input after ''frame:'
  try:
    ls = frame.split(': ', 1)
    if len(ls) != 2:
      raise SyntaxError('Invalid Configuration File: frame should be in format widthxheight!')
  except SyntaxError as se:
    print(se)
    f_battle.close()
    exit()

    #Check if the content after 'frame:' is appropriate
  try:
    ls = frame.split(': ', 1)
    content = str(ls[1])
    con_ls = list(content)
    con_ls.remove('\n')
    if len(con_ls) != 3:
      raise SyntaxError('Invalid Configuration File: frame should be in format widthxheight!')
    width = con_ls[0]
    height = con_ls[2]
    if width.isdigit() == False or height.isdigit() == False:
      raise SyntaxError('Invalid Configuration File: frame should be in format widthxheight!')
    if con_ls[1] != 'x':
      raise SyntaxError('Invalid Configuration File: frame should be in format widthxheight!')
  except SyntaxError as se:
    print(se)
    f_battle.close()
    exit()

#------------------------------------------------------------------------  
def test_frame_out_of_range(filepath):
  # add "format_out_of_range_file.txt" in "invalid_files"
  f_battle = open(filepath, "r")
  frame = f_battle.readline()
  content_ls = list(frame[7:])

    #Determine whether the length and width are within the range
  try:
    width = int(content_ls[0])
    height = int(content_ls[2])
    if width < 5 or width >7:
      raise ArithmeticError('Invalid Configuration File: width and height should range from 5 to 7!')
    if height <5 or height >7:
      raise ArithmeticError('Invalid Configuration File: width and height should range from 5 to 7!')
  except ArithmeticError as ae:
      print(ae)
      f_battle.close()
      exit()   

#------------------------------------------------------------------------ 
def test_non_integer(filepath):
  # add "non_integer_file.txt" in "invalid_files"
  f_battle = open(filepath, "r")
  frame = f_battle.readline()
  ls = ['Frame', 'Water', 'Wood', 'Food', 'Gold']
  i = 1
  #Check whether the input after the label is an integer
  try:
    while i<5:
      each_l = f_battle.readline()
      content = each_l.split(': ', 1)
      if content[1] == '\n':
        pass 
      else:
        check_con = content[1]
        check_con = check_con.replace('\n', '')
        check_con = check_con.replace(' ', '')
        if check_con.isdigit() == False:
          raise ValueError(f'Invalid Configuration File: {ls[i]} contains non integer characters!')
      i += 1
  except ValueError as ae:
    print(ae)
    f_battle.close()
    exit() 
          
#------------------------------------------------------------------------ 
def test_out_of_map(filepath):
  # add "out_of_map_file.txt" in "invalid_files"
  f_battle = open(filepath, "r")
  frame = f_battle.readline()

  #Display the width and height of the map
  frame_con = frame.split(': ', 1)
  width = int(frame_con[1][0])
  height = int(frame_con[1][2])

  #Check whether the input content is within the range of the map
  ls = ['Frame', 'Water', 'Wood', 'Food', 'Gold']
  i = 1
  try:
    while i<5:
      each_l = f_battle.readline()
      each_l = each_l.rstrip()
      content = each_l.split(': ', 1)
      if len(content) == 1:
        pass
      else:
        con_ls = content[1].split(' ')
        for a in range(len(con_ls)):
          if a%2 == 0:
            if int(con_ls[a]) > width-1:
              raise ArithmeticError(f'Invalid Configuration File: {ls[i]} contains a position that is out of map.')
          else:
            if int(con_ls[a]) > height-1:
              raise ArithmeticError(f'Invalid Configuration File: {ls[i]} contains a position that is out of map.')
      i += 1
  except ArithmeticError as ae:
    print(ae)
    f_battle.close()
    exit() 

#------------------------------------------------------------------------ 
def test_occupy_home_or_next_to_home(filepath):
  # add two invalid files: "occupy_home_file.txt" and
  # "occupy_next_to_home_file.txt" in "invalid_files"
  f_battle = open(filepath, "r")
  frame = f_battle.readline()
  width_f = int(frame[7])
  height_f = int(frame[9])

  #Convert input into coordinate form
  i = 1
  try:
    while i<5:
      each_l = f_battle.readline()
      each_l = each_l.rstrip()
      content = each_l.split(': ', 1)
      if len(content) == 1:
        pass
      else:
        con_ls = content[1].split(' ')
        width_ls = []
        height_ls = []
        for i in range(len(con_ls)):
          if i%2 == 0:
            width_ls.append(con_ls[i])
          else:
            height_ls.append(con_ls[i])
        position_ls = list(zip(width_ls, height_ls))
    

    
    #Check if the coordinates occupy the base    
        for a in range(len(position_ls)):
          if int(position_ls[a][0]) == 1 and int(position_ls[a][1]) == 1 or int(position_ls[a][0]) == width_f-2 and int(position_ls[a][1]) == height_f-2:
            raise ValueError('Invalid Configuration File: The positions of home bases or thepositions next to the home bases are occupied!')
    #Check if the coordinates occupy the the surrounding positions
          if int(position_ls[a][0]) == 0 and int(position_ls[a][1]) == 1 or int(position_ls[a][0]) == width_f-3 and int(position_ls[a][1]) == height_f-2:
            raise ValueError('Invalid Configuration File: The positions of home bases or thepositions next to the home bases are occupied!')
          if int(position_ls[a][0]) == 1 and int(position_ls[a][1]) == 0 or int(position_ls[a][0]) == width_f-2 and int(position_ls[a][1]) == height_f-3:
            raise ValueError('Invalid Configuration File: The positions of home bases or thepositions next to the home bases are occupied!')
          if int(position_ls[a][0]) == 2 and int(position_ls[a][1]) == 1 or int(position_ls[a][0]) == width_f-1 and int(position_ls[a][1]) == height_f-2:
            raise ValueError('Invalid Configuration File: The positions of home bases or thepositions next to the home bases are occupied!')
          if int(position_ls[a][0]) == 1 and int(position_ls[a][1]) == 2 or int(position_ls[a][0]) == width_f-2 and int(position_ls[a][1]) == height_f-1:
            raise ValueError('Invalid Configuration File: The positions of home bases or thepositions next to the home bases are occupied!')   
      i += 1
  except ValueError as vae:
    print(vae)
    f_battle.close()
    exit()

#------------------------------------------------------------------------
def test_duplicate_position(filepath):
  # add two files: "dupli_pos_in_single_line.txt" and
  # "dupli_pos_in_multiple_lines.txt" in "invalid_files"
  f_battle = open(filepath, "r")
  frame = f_battle.readline()
  #Convert input into coordinate form
  i = 1
  total_ls = []
  
  while i<5:
    each_l = f_battle.readline()
    each_l = each_l.strip()
    content = each_l.split(': ', 1)
    if len(content) == 1:
      pass
    else:
      con_ls = content[1].split(' ')
      width_ls = []
      height_ls = []
      for u in range(len(con_ls)):
        if u%2 == 0:
          width_ls.append(con_ls[u])
        else:
          height_ls.append(con_ls[u])
      position_ls = list(zip(width_ls, height_ls))
      total_ls.append(position_ls)
    i +=1 
  
  #dupli_pos_in_single_line
  if len(total_ls) == 0:
    pass
  else: 
    try:  
      for a in range(len(total_ls)):
        single_l = total_ls[a]
        count_of_pos_single = dict(Counter(single_l))
        dupli_pos_ls = [key for key, value in count_of_pos_single.items() if value >1]       
        if len(dupli_pos_ls) != 0:
          dupli_pos = dupli_pos_ls[0]
          raise SyntaxError(f'Invalid Configuration File: Duplicate position {dupli_pos}!')

    except SyntaxError as se:
      print(se)
      f_battle.close()
      exit()

    #dupli_pos_in_multiple_lines
    try:
      if len(total_ls) == 0 or len(total_ls) == 1:
        pass

      if len(total_ls) == 2:
        mul_l_1, mul_l_2 = set(total_ls[0]), set(total_ls[1])
        mul_pos_2 = mul_l_2 & mul_l_1
        if len(mul_pos_2) != 0:
          dupli_pos_mul = list(mul_pos_2)
          raise SyntaxError(f'Invalid Configuration File: Duplicate position {dupli_pos_mul[0]}!')

      if len(total_ls) == 3:
        mul_l_1, mul_l_2, mul_l_3 = set(total_ls[0]), set(total_ls[1]), set(total_ls[2])
        mul_pos_a, mul_pos_b, mul_pos_c = mul_l_1 & mul_l_2, mul_l_1 & mul_l_3, mul_l_2 & mul_l_3
        if len(mul_pos_a) != 0:
          dupli_pos_mul = list(mul_pos_a)
          raise SyntaxError(f'Invalid Configuration File: Duplicate position {dupli_pos_mul[0]}!')
        if len(mul_pos_b) != 0:
          dupli_pos_mul = list(mul_pos_b)
          raise SyntaxError(f'Invalid Configuration File: Duplicate position {dupli_pos_mul[0]}!')
        if len(mul_pos_c) != 0:
          dupli_pos_mul = list(mul_pos_c)
          raise SyntaxError(f'Invalid Configuration File: Duplicate position {dupli_pos_mul[0]}!')

      if len(total_ls) == 4:
        mul_l_1, mul_l_2, mul_l_3, mul_l_4 = set(total_ls[0]), set(total_ls[1]), set(total_ls[2]), set(total_ls[3])
        mul_pos_a, mul_pos_b, mul_pos_c = mul_l_1 & mul_l_2, mul_l_1 & mul_l_3, mul_l_1 & mul_l_4
        mul_pos_d, mul_pos_e, mul_pos_f = mul_l_2 & mul_l_3, mul_l_2 & mul_l_4, mul_l_2 & mul_l_4
        if len(mul_pos_a) != 0:
          dupli_pos_mul = list(mul_pos_a)
          raise SyntaxError(f'Invalid Configuration File: Duplicate position {dupli_pos_mul[0]}!')
        if len(mul_pos_b) != 0:
          dupli_pos_mul = list(mul_pos_b)
          raise SyntaxError(f'Invalid Configuration File: Duplicate position {dupli_pos_mul[0]}!')
        if len(mul_pos_c) != 0:
          dupli_pos_mul = list(mul_pos_c)
          raise SyntaxError(f'Invalid Configuration File: Duplicate position {dupli_pos_mul[0]}!')
        if len(mul_pos_d) != 0:
          dupli_pos_mul = list(mul_pos_d)
          raise SyntaxError(f'Invalid Configuration File: Duplicate position {dupli_pos_mul[0]}!')
        if len(mul_pos_e) != 0:
          dupli_pos_mul = list(mul_pos_e)
          raise SyntaxError(f'Invalid Configuration File: Duplicate position {dupli_pos_mul[0]}!')    
        if len(mul_pos_f) != 0:
          dupli_pos_mul = list(mul_pos_f)
          raise SyntaxError(f'Invalid Configuration File: Duplicate position {dupli_pos_mul[0]}!')      
    except SyntaxError as se:
      print(se)
      f_battle.close()
      exit()    

#------------------------------------------------------------------------
def test_odd_length(filepath):
  # add "odd_length_file.txt" in "invalid_files"
  f_battle = open(filepath, "r")
  frame = f_battle.readline()
  ls = ['Frame', 'Water', 'Wood', 'Food', 'Gold']
  i = 1
  #Check whether the number of integers entered after the label is an even number
  try:
    while i<5:
      each_l = f_battle.readline()
      content = each_l.split(': ', 1)
      check_con = content[1]
      check_con = check_con.rstrip()
      check_ls = check_con.split(' ')
      if len(check_ls) == 1 and check_ls[0] == '':
        pass
      elif len(check_ls)%2 != 0:
        raise SyntaxError(f'Invalid Configuration File: {ls[i]} has an odd number of elements!')
    
      i += 1
  except SyntaxError as se:
    print(se)
    f_battle.close()
    exit() 
              
#------------------------------------------------------------------------
def test_valid_file(filepath):
  # no need to create file for this one, just test loading config.txt
  print(f'Configuration file {filepath} was loaded.')

# you can run this test file to check tests and load_config_file
if __name__ == "__main__":
  test_file_not_found(filepath)
  test_format_error(filepath)
  test_frame_format_error(filepath)
  test_frame_out_of_range(filepath)
  test_non_integer(filepath)
  test_odd_length(filepath)
  test_out_of_map(filepath)
  test_occupy_home_or_next_to_home(filepath)
  test_duplicate_position(filepath)
  test_valid_file(filepath)