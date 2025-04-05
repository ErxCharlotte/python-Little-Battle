import sys
from collections import Counter
#Some definition
  #About soilder prices (name, wood, food, gold)
S = [('Spearman'), (1), (1), (0)]
A = [('Archer'), (1), (0), (1)]
K = [('Knight'), (0), (1), (1)]
T = [('Scout'), (1), (1), (1)]

  #Origin resources that user hold (waters, woods, foods, golds)
resources_hold_1 = [2, 2, 2]
resources_hold_2 = [2, 2, 2]
  
  #The first year of the game
now_year, player= 617, 1
  #army information on the map
soi_type_and_pos_1 = []
soi_type_and_pos_2 = []

tot_soi_type_and_pos = [soi_type_and_pos_1, soi_type_and_pos_2]

  #The counters relationship (kill / be killed)
S_counter = [['Knight', 'Scout'], ['Archer']]
K_counter = [['Archer', 'Scout'], ['Spearman']]
A_counter = [['Spearman', 'Scout'], ['Knight']]
T_counter = [[''], ['Spearman', 'Knight', 'Archer']]

#------------------------------------------------------------------------ 
#Check the file whether vaild
def load_config_file(filepath):
  try:
    f_battle = open(filepath, "r")
  except FileNotFoundError:
    raise FileNotFoundError('The file not found')

  try:
    #test_format_error
    f_battle = open(filepath, "r")
    ls = f_battle.readlines()
    if len(ls) != 5:
      raise SyntaxError('Invalid Configuration File: format error!')
    f_battle.close()

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


    #test_frame_format_error
    f_battle = open(filepath, "r")
    frame = f_battle.readline()
      #Check if there is any input after ''frame:'
    ls = frame.split(': ', 1)
    if len(ls) != 2:
      raise SyntaxError('Invalid Configuration File: frame should be in format widthxheight!')
      #Check if the content after 'frame:' is appropriate
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
    f_battle.close()
  

    #test_frame_out_of_range
    f_battle = open(filepath, "r")
    frame = f_battle.readline()
    content_ls = list(frame[7:])
      #Determine whether the length and width are within the range
    width = int(content_ls[0])
    height = int(content_ls[2])
    if width < 5 or width >7:
      raise ArithmeticError('Invalid Configuration File: width and height should range from 5 to 7!')
    if height <5 or height >7:
      raise ArithmeticError('Invalid Configuration File: width and height should range from 5 to 7!')
    f_battle.close()
 

    #test_non_integer
    f_battle = open(filepath, "r")
    frame = f_battle.readline()
    ls = ['Frame', 'Water', 'Wood', 'Food', 'Gold']
    i = 1
      #Check whether the input after the label is an integer
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
    f_battle.close()


    #test_odd_length
    f_battle = open(filepath, "r")
    frame = f_battle.readline()
    ls = ['Frame', 'Water', 'Wood', 'Food', 'Gold']
    i = 1
      #Check whether the number of integers entered after the label is an even number
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
    f_battle.close()


    #test_out_of_map
    f_battle = open(filepath, "r")
    frame = f_battle.readline()
      #Display the width and height of the map
    frame_con = frame.split(': ', 1)
    width = int(frame_con[1][0])
    height = int(frame_con[1][2])
      #Check whether the input content is within the range of the map
    ls = ['Frame', 'Water', 'Wood', 'Food', 'Gold']
    i = 1
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
    f_battle.close()


    #test_occupy_home_or_next_to_home
    f_battle = open(filepath, "r")
    frame = f_battle.readline()
    width_f = int(frame[7])
    height_f = int(frame[9])
      #Convert input into coordinate form
    i = 1
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
    f_battle.close()


    #test_duplicate_position
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
      for a in range(len(total_ls)):
        single_l = total_ls[a]
        count_of_pos_single = dict(Counter(single_l))
        dupli_pos_ls = [key for key, value in count_of_pos_single.items() if value >1]       
        if len(dupli_pos_ls) != 0:
          dupli_pos = dupli_pos_ls[0]
          raise SyntaxError(f'Invalid Configuration File: Duplicate position {dupli_pos}!')
      f_battle.close()
        #dupli_pos_in_multiple_lines
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
        f_battle.close()  


#------------------------------------------------------------------------
#Load the file to find the imformation 
def load_infomation(filepath):
  f_battle = open(filepath, 'r')

  #return width and height based on the file
  frame = f_battle.readline()
  width, height = int(frame[7]), int(frame[9])
  base_2 = (width - 2, height - 2)
  bases = [(1,1), base_2]

  #return resources lists of position tuples
  resource_ls = []
  for i in range(4):
    resource_content = f_battle.readline()
    resource_content = resource_content.rstrip()
    content_ls = resource_content.split(': ', 1)
    if len(content_ls) == 1:
      resource_ls.append([])
    else:
      con_pos_ls = content_ls[1].split(' ')
      width_ls = []
      height_ls = []
      for a in range(len(con_pos_ls)):
        if a%2 == 0:
          width_ls.append(int(con_pos_ls[a]))
        else:
          height_ls.append(int(con_pos_ls[a]))
      position_ls = list(zip(width_ls, height_ls))
      resource_ls.append(position_ls)
  waters, woods, foods, golds = resource_ls[0], resource_ls[1], resource_ls[2], resource_ls[3]
  f_battle.close()

  resources_ls = [waters, woods, foods, golds]
  
  return width, height, waters, woods, foods, golds, bases, resources_ls
#------------------------------------------------------------------------ 
#when the input equal to 'QUIT' (exit the program)
def QUIT():
  exit()

#------------------------------------------------------------------------ 
#when the input equal to 'PRIS' (print out the price of the army)
def PRIS():
  print('Recruit Prices:\n  Spearman (S) - 1W, 1F\n  Archer (A) - 1W, 1G\n  Knight (K) - 1F, 1G\n  Scout (T) - 1W, 1F, 1G')

#------------------------------------------------------------------------ 
#find out the origin lines with bases (without army and resources)
def find_origin_lines(width, height):
  print('Please check the battlefield, commander.')

  #The first line of the map
  first_ls = []
  for i in range(width):
    if i == 0:
      first_ls.append('  X00')
    elif i == width - 1:
      first_ls.append(f' 0{i}X')
    else:
      first_ls.append(f' 0{i}')
  first_l = ''.join(first_ls)
  print(first_l)
  #The second line of the map
  second_ls = [' Y+']
  row_of_sym = '-' * (width * 3 - 1)
  second_ls.append(row_of_sym)
  second_ls.append('+')
  second_l = ''.join(second_ls)
  print(second_l)

  #The lines with resources of the map
  total_ls = []
  for a in range(height):
    re_l_ls = [f'0{a}|']
    row_re_l = '  |' * width
    re_l_ls.append(row_re_l)
    re_l = ''.join(re_l_ls)
    total_ls.append(re_l)
    if a == 1:
      base_1_pos = total_ls[1][:6] + 'H1' + total_ls[1][8:]
      total_ls[1] = base_1_pos
    if a == height - 2:
      base_2_pos = total_ls[a][:3*width-3] +'H2' + total_ls[a][3*width-1:]
      total_ls[a] = base_2_pos

  return total_ls, second_l, first_l

#------------------------------------------------------------------------ 
#find out the position of the resources and their symbol
def resources_pos_symbol(resources, waters, woods, foods, golds):
  if len(resources) == 0:
    pass
  else:
    width_re_ls = []
    height_re_ls = []
    for i in range(len(resources)):
      width_re_ls.append(int(resources[i][0]))
      height_re_ls.append(int(resources[i][1]))
    if resources == waters:
      symbol = '~~'
    elif resources == woods:
      symbol = 'WW'
    elif resources == foods:
      symbol = 'FF'
    elif resources == golds:
      symbol = 'GG'

  return width_re_ls, height_re_ls, symbol

#------------------------------------------------------------------------
#display the map with resources
def map_with_re_lines(total_ls, width_ls, height_ls, symbol):
  for u in range(len(width_ls)):
    change_line = total_ls[height_ls[u]]
    change_l_after = change_line[:3*width_ls[u]+3] + symbol + change_line[3*width_ls[u]+5:]
    total_ls[height_ls[u]] = change_l_after

  return total_ls

#------------------------------------------------------------------------
#display the origin map without soilder
def map_origin(re_total_ls, second_l):
  origin_map_ls = re_total_ls[:]
  for p in range(len(origin_map_ls)):
    print(origin_map_ls[p])
  print(second_l)
  return origin_map_ls

#------------------------------------------------------------------------
#display the origin map (without anything)
def map_without_any(width,height):
  map_without_any_ls = []
  for a in range(height):
    re_l_ls = [f'0{a}|']
    row_re_l = '  |' * width
    re_l_ls.append(row_re_l)
    re_l = ''.join(re_l_ls)
    map_without_any_ls.append(re_l)
    if a == 1:
      base_1_pos = map_without_any_ls[1][:6] + 'H1' + map_without_any_ls[1][8:]
      map_without_any_ls[1] = base_1_pos
    if a == width - 2:
      base_2_pos = map_without_any_ls[a][:3*width-3] +'H2' + map_without_any_ls[a][3*width-1:]
      map_without_any_ls[a] = base_2_pos
  return map_without_any_ls

#------------------------------------------------------------------------
#difference the player 1 and player 2
def difference_player(player, width, height):
  if player % 2 != 0:
    player = 1
    resources_hold = resources_hold_1
    soi_type_and_pos = soi_type_and_pos_1
    soi_type_and_pos_enemy = soi_type_and_pos_2
    next_to_base = [(0,1),(1,0),(2,1),(1,2)]
    base = (1,1)
    base_enemy = (width-2, height-2)
  else:
    player = 2
    resources_hold = resources_hold_2
    soi_type_and_pos = soi_type_and_pos_2
    soi_type_and_pos_enemy = soi_type_and_pos_1
    next_to_base = [(width-3,height-2),(width-2,height-3),(width-1,height-2),(width-2,height-1)]
    base = (width-2, height-2)
    base_enemy = (1,1)

  return player, resources_hold, soi_type_and_pos, next_to_base, soi_type_and_pos_enemy, base, base_enemy

#------------------------------------------------------------------------
#print out the now year (for each turns)
def print_year_stage(now_year, player):
  print(f'-Year {now_year}-\n')
  print(f"+++Player {player}'s Stage: Recruit Armies+++\n")

#------------------------------------------------------------------------
#print out the resources that player asset
def asset_resources(resources_hold):
  print(f'[Your Asset: Wood - {resources_hold[0]} Food - {resources_hold[1]} Gold - {resources_hold[2]}]')

#------------------------------------------------------------------------
#check the asset resources or the places whether enough
def check_resources_places(resources_hold):
  #find the resources whether enough to recruit
  is_enough = False
  count_zero = 0
  for a in range(3):
    if resources_hold[a] == 0:
      count_zero += 1
  if count_zero < 2:
      is_enough = True
  else:
      is_enough = False
      print('No resources to recruit any armies.')
    
  return is_enough

#------------------------------------------------------------------------
#match the user input with the armies
def match_army(user_input):
  if user_input == 'S':
    army_ls = S
  elif user_input == 'A':
    army_ls = A
  elif user_input == 'K':
    army_ls = K 
  elif user_input == 'T':
    army_ls = T
  return army_ls

#------------------------------------------------------------------------
#apply the cost for recruit the army
def apply_cost(resources_hold, army_ls):
  for i in range(1,4):
    resources_hold[i-1] = resources_hold[i-1] - army_ls[i]
  return resources_hold 

#------------------------------------------------------------------------
#record the position and the type of army for the recruit
def record_pos_type(army_ls, army_placein_ls, soi_type_and_pos):
  army_width = int(army_placein_ls[0])
  army_height = int(army_placein_ls[1])
  army_position = (army_width, army_height)
  army_type = army_ls[0]
  infomation_ls = [army_type, army_position]
  soi_type_and_pos.append(infomation_ls)

  return soi_type_and_pos

#------------------------------------------------------------------------
#apply the army position into the map
def apply_position(map_without_any_ls, tot_soi_type_and_pos, player, resources_ls):
  width_ls, height_ls, symbol_ls = [], [], []
  tot_soi_type_and_pos = [soi_type_and_pos_1, soi_type_and_pos_2]
  if len(tot_soi_type_and_pos[1]) == 0:
    stop_num = 1
  else:
    stop_num = 2

  for i in range(stop_num):
    for p in range(len(tot_soi_type_and_pos[i])):
      width_ls.append(tot_soi_type_and_pos[i][p][1][0])
      height_ls.append(tot_soi_type_and_pos[i][p][1][1])
  
  for m in range(stop_num):
    if m == 0:
      player_num = 1
    if m == 1:
      player_num = 2

    for a in range(len(tot_soi_type_and_pos[m])):
      if tot_soi_type_and_pos[m][a][0] == 'Archer':
        symbol_ls.append(f'A{player_num}')
      if tot_soi_type_and_pos[m][a][0] == 'Spearman':
        symbol_ls.append(f'S{player_num}')
      if tot_soi_type_and_pos[m][a][0] == 'Knight':
        symbol_ls.append(f'K{player_num}')
      if tot_soi_type_and_pos[m][a][0] == 'Scout':
        symbol_ls.append(f'T{player_num}')

  for u in range(len(resources_ls)):
    if u == 0:
      resource_symbol = '~~'
    elif u == 1:
      resource_symbol = 'WW'
    elif u == 2:
      resource_symbol = 'FF'
    elif u == 3:
      resource_symbol = 'GG'

    for b in range(len(resources_ls[u])):
      width_ls.append(resources_ls[u][b][0])
      height_ls.append(resources_ls[u][b][1]) 
      symbol_ls.append(resource_symbol)

  use_for_copy_ls = map_without_any_ls[:]
  for q in range(len(width_ls)):
    change_line = use_for_copy_ls[height_ls[q]]
    change_l_after = change_line[:3*width_ls[q]+3] + symbol_ls[q] + change_line[3*width_ls[q]+5:]
    use_for_copy_ls[height_ls[q]] = change_l_after
    map_ls = use_for_copy_ls[:]  	

  return map_ls

#------------------------------------------------------------------------
#check the user input of the position of the army whether next to the home base or occupied
def check_posin(army_placein_ls, soi_type_and_pos, next_to_base, soi_type_and_pos_enemy):
  posin_vaild = True
  army_width = int(army_placein_ls[0])
  army_height = int(army_placein_ls[1])
  position_army = (army_width, army_height)
  
  #Not next to the home base
  if position_army not in next_to_base:
    posin_vaild = False
    print('You must place your newly recruited unit in an unoccupied position next to your home base. Try again.')
  #the position is occupied
  if len(soi_type_and_pos) == 0 and len(soi_type_and_pos_enemy) == 0:
    pass
  else:
    for i in range(len(soi_type_and_pos)):
      if position_army == soi_type_and_pos[i][1]:
        posin_vaild = False
        print('You must place your newly recruited unit in an unoccupied position next to your home base. Try again.')
    for a in range(len(soi_type_and_pos_enemy)):
      if position_army == soi_type_and_pos_enemy[a][1]:
        posin_vaild = False
        print('You must place your newly recruited unit in an unoccupied position next to your home base. Try again.')
  return posin_vaild
    
#------------------------------------------------------------------------
#check whether the all four positions next to the home base are occupied
def check_next_to_base_occupied(next_to_base, soi_type_and_pos, soi_type_and_pos_enemy):
  all_four_pos_occupied = False
  count = 0
  for i in range(len(soi_type_and_pos)):
    if soi_type_and_pos[i][1] in next_to_base:
      count += 1
  for a in range(len(soi_type_and_pos_enemy)):
    if soi_type_and_pos_enemy[a][1] in next_to_base:
      count += 1
  if count == 4:
    all_four_pos_occupied = True
    print('No place to recruit new armies.')
  return all_four_pos_occupied

#------------------------------------------------------------------------
#check whether the resources enought to recruit the army
def enough_to_recruit(resources_hold, army_ls):
  recruit_enough = True
  for i in range(1,4):
    if resources_hold[i-1] < army_ls[i]:
      recruit_enough = False
      print('Insufficient resources. Try again.')
  return recruit_enough

#------------------------------------------------------------------------
#print armies to move
def print_armies(soi_type_and_pos):
  one_round_armies = soi_type_and_pos[:]
  s_pos_ls = []
  a_pos_ls = []
  k_pos_ls = []
  t_pos_ls = []

  for i in range(len(one_round_armies)):
    if one_round_armies[i][0] == 'Archer':
      a_pos_ls.append(str(one_round_armies[i][1]))
    if one_round_armies[i][0] == 'Spearman':
      s_pos_ls.append(str(one_round_armies[i][1]))
    if one_round_armies[i][0] == 'Knight':
      k_pos_ls.append(str(one_round_armies[i][1]))
    if one_round_armies[i][0] == 'Scout':
      t_pos_ls.append(str(one_round_armies[i][1]))
 
  #print out the armies
  print('Armies to Move:')
  if len(s_pos_ls) != 0:
    print('  Spearman: ' + ', '.join(s_pos_ls))
  if len(a_pos_ls) != 0:
    print('  Archer: ' + ', '.join(a_pos_ls))
  if len(k_pos_ls) != 0:
    print('  Knight: ' + ', '.join(k_pos_ls))
  if len(t_pos_ls) != 0:
    print('  Scout: ' + ', '.join(t_pos_ls))

  return one_round_armies

#------------------------------------------------------------------------
#according to the user input to find the start move position and the end move position
def start_end_pos(army_movein_ls):
  start_width = int(army_movein_ls[0])
  start_height = int(army_movein_ls[1])
  end_width = int(army_movein_ls[2])
  end_height = int(army_movein_ls[3])

  start_move = (start_width, start_height)
  end_move = (end_width, end_height)
  return start_move, end_move

#------------------------------------------------------------------------
#according to the user input to find which army will be move
def army_will_move(start_move, end_move, soi_type_and_pos, one_round_armies):
  use_for_copy_ls = one_round_armies[:]
  for q in range(len(one_round_armies)):
    if start_move == one_round_armies[q][1]:
      use_for_copy_ls.remove(one_round_armies[q]) 

  for i in range(len(soi_type_and_pos)):
    if start_move == soi_type_and_pos[i][1]:
      army_name = soi_type_and_pos[i][0]
      soi_type_and_pos[i][1] = end_move
  return soi_type_and_pos, army_name, use_for_copy_ls

#------------------------------------------------------------------------
#check the move of the army whether move to the other armies
def check_other_armies(end_move, soi_type_and_pos, base):
  have_other_armies = False
  for i in range(len(soi_type_and_pos)):
    if end_move == soi_type_and_pos[i][1] or end_move == base:
      have_other_armies = True
  return have_other_armies
      
#------------------------------------------------------------------------
#find that the army move to a resource
def move_to_resource(start_move, end_move, resources_ls, resources_hold, scout_die_between):
  #copy a new list for use
  copy_re_ls = [[],[],[],[]]
  for p in range(4):
    for u in range(len(resources_ls[p])):
      copy_re_ls[p].append(resources_ls[p][u])

  if scout_die_between == True:
    pass
  else:
    for i in range(1,4):
      if i == 1:
        resource_name = 'Wood'
      if i == 2:
        resource_name = 'Food'
      if i == 3:
        resource_name = 'Gold'

      between_move = ''
      if abs(start_move[0] - end_move[0]) == 2:
        between_move = (min(start_move[0], end_move[0]) + 1 , start_move[1])
      elif abs(start_move[1] - end_move[1]) == 2:
        between_move = (start_move[0] , min(start_move[1], end_move[1]) + 1)

      for a in range(len(resources_ls[i])):
        if end_move == resources_ls[i][a] or  between_move == resources_ls[i][a]:
          copy_re_ls[i].remove(resources_ls[i][a])
          resources_hold[i-1] = resources_hold[i-1] + 2
          print(f'Good. We collected 2 {resource_name}.')

  return copy_re_ls, resources_hold

#------------------------------------------------------------------------
#find that the army move to the water
def move_to_water(start_move, end_move, resources_ls, soi_type_and_pos, soi_type_and_pos_enemy, scout_die_between):
  copy_ls_self = soi_type_and_pos[:]
  copy_ls_enemy = soi_type_and_pos_enemy[:]

  between_move = ''
  if abs(start_move[0] - end_move[0]) == 2:
    between_move = (min(start_move[0], end_move[0]) + 1 , start_move[1])
  elif abs(start_move[1] - end_move[1]) == 2:
    between_move = (start_move[0] , min(start_move[1], end_move[1]) + 1)

  for i in range(len(resources_ls[0])):
    if between_move == resources_ls[0][i]:
      for a in range(len(soi_type_and_pos)):
        if end_move == soi_type_and_pos[a][1]:
          army_name = soi_type_and_pos[a][0]
          copy_ls_self.remove(soi_type_and_pos[a])
          print(f'We lost the army {army_name} due to your command!')
          scout_die_between = True
      break

    if end_move == resources_ls[0][i]:
      for b in range(len(soi_type_and_pos)):
        if end_move == soi_type_and_pos[b][1]:
          army_name = soi_type_and_pos[b][0]
          copy_ls_self.remove(soi_type_and_pos[b])
          print(f'We lost the army {army_name} due to your command!')

  return copy_ls_self, copy_ls_enemy, scout_die_between
  
#------------------------------------------------------------------------
#find that the army move to other army of same type
def move_to_same_type_army(player, end_move, army_name, soi_type_and_pos, soi_type_and_pos_enemy):
  copy_ls_self = soi_type_and_pos[:]
  copy_ls_enemy = soi_type_and_pos_enemy[:]

  for i in range(len(soi_type_and_pos_enemy)):
    if army_name == 'Scout':
      pass
    else:
      if end_move == soi_type_and_pos_enemy[i][1] and army_name == soi_type_and_pos_enemy[i][0]:
        print(f'We destroyed the enemy {army_name} with massive loss!')
        copy_ls_enemy.remove(soi_type_and_pos_enemy[i])
        for a in range(len(soi_type_and_pos)):
          if end_move == soi_type_and_pos[a][1]:
            copy_ls_self.remove(soi_type_and_pos[a])

  return copy_ls_self, copy_ls_enemy

#------------------------------------------------------------------------
#find that the army move to other army which will kill the other amry
def move_to_kill_other_army(player, end_move, army_name, soi_type_and_pos, soi_type_and_pos_enemy):
  copy_ls_self = soi_type_and_pos[:]
  copy_ls_enemy = soi_type_and_pos_enemy[:]

  #match the counter list
  if army_name == 'Spearman':
    counter_ls = S_counter
  if army_name == 'Archer':
    counter_ls = A_counter
  if army_name == 'Knight':
    counter_ls = K_counter

  if army_name == 'Scout':
    pass
  else:
    for i in range(len(soi_type_and_pos_enemy)):
      if end_move == soi_type_and_pos_enemy[i][1] and soi_type_and_pos_enemy[i][0] in counter_ls[0]:
        print(f'Great! We defeated the enemy {soi_type_and_pos_enemy[i][0]}!')
        copy_ls_enemy.remove(soi_type_and_pos_enemy[i])

  return copy_ls_self, copy_ls_enemy

#------------------------------------------------------------------------
#find that the army move to other army which will kill self army
def move_to_be_killed_army(player, end_move, army_name, soi_type_and_pos, soi_type_and_pos_enemy):
  copy_ls_self = soi_type_and_pos[:]
  copy_ls_enemy = soi_type_and_pos_enemy[:]

  #match the counter list
  if army_name == 'Spearman':
    counter_ls = S_counter
  if army_name == 'Archer':
    counter_ls = A_counter
  if army_name == 'Knight':
    counter_ls = K_counter
    
  if army_name == 'Scout':
    pass

  else:
    for i in range(len(soi_type_and_pos_enemy)):
      if end_move == soi_type_and_pos_enemy[i][1] and soi_type_and_pos_enemy[i][0] in counter_ls[1]:
        print(f'We lost the army {army_name} due to your command!')
        for b in range(len(soi_type_and_pos)):
          if end_move == soi_type_and_pos[b][1]:
            copy_ls_self.remove(soi_type_and_pos[b])        

  return copy_ls_self, copy_ls_enemy

#------------------------------------------------------------------------
#layer win the game
def win_game(player, end_move, army_name, now_year, scout_die_between, base_enemy):
  between_move = ''
  if abs(start_move[0] - end_move[0]) == 2:
    between_move = (min(start_move[0], end_move[0]) + 1 , start_move[1])
  elif abs(start_move[1] - end_move[1]) == 2:
    between_move = (start_move[0] , min(start_move[1], end_move[1]) + 1)

  if scout_die_between == True:
    pass
  else:
    if end_move == base_enemy or between_move == base_enemy:
      print(f'The army {army_name} captured the enemy’s capital.\n')
      commander_name = input('What’s your name, commander?\n')
      print(f'\n***Congratulation! Emperor {commander_name} unified the country in {now_year}.***')
      exit()

#------------------------------------------------------------------------
#limit the direction of steps the player can take
def limit_direction(start_move, end_move):
  correct_direction = True
  if start_move[0] != end_move[0] and start_move[1] != end_move[1]:
    correct_direction = False
  return correct_direction

#------------------------------------------------------------------------
#limit the time of steps the player can take
def limit_one_step(start_move, end_move, soi_type_and_pos):
  correct_step = False
  army_name = ''
  for i in range(len(soi_type_and_pos)):
    if start_move == soi_type_and_pos[i][1]:
      army_name = soi_type_and_pos[i][0]
  
  if army_name == 'Scout':
    if 0 < abs(end_move[0]-start_move[0]) < 3 or 0 < abs(end_move[1]-start_move[1]) < 3:
      correct_step = True
  else:
    if 0 < abs(end_move[0]-start_move[0]) < 2 or 0 < abs(end_move[1]-start_move[1]) < 2:
      correct_step = True
  return correct_step

#------------------------------------------------------------------------
#destroy the Scout
def destroy_scout(start_move, end_move, army_name, soi_type_and_pos, soi_type_and_pos_enemy, scout_die_between):
  between_move = ''
  copy_ls_self = soi_type_and_pos[:]
  copy_ls_enemy = soi_type_and_pos_enemy[:]

  if army_name == 'Scout':
    if abs(start_move[0] - end_move[0]) == 2:
      between_move = (min(start_move[0], end_move[0]) + 1 , start_move[1])
    elif abs(start_move[1] - end_move[1]) == 2:
      between_move = (start_move[0] , min(start_move[1], end_move[1]) + 1)

    for i in range(len(soi_type_and_pos_enemy)):
      if between_move == soi_type_and_pos_enemy[i][1]:
        if soi_type_and_pos_enemy[i][0] == 'Scout':
          copy_ls_enemy.remove(soi_type_and_pos_enemy[i])
          print('We destroyed the enemy Scout with massive loss!')
        else:
          print('We lost the army Scout due to your command!')

        for a in range(len(soi_type_and_pos)):
          if end_move == soi_type_and_pos[a][1]:
            copy_ls_self.remove(soi_type_and_pos[a])
        scout_die_between = True

    if between_move == base_enemy:
      pass
    elif scout_die_between == True:
      pass
    else:
      for p in range(len(soi_type_and_pos_enemy)):
        if end_move == soi_type_and_pos_enemy[p][1]:
          if soi_type_and_pos_enemy[p][0] == 'Scout':
            copy_ls_enemy.remove(soi_type_and_pos_enemy[p])
            print('We destroyed the enemy Scout with massive loss!')
          else:
            print('We lost the army Scout due to your command!')

          for b in range(len(soi_type_and_pos)):
            if end_move == soi_type_and_pos[b][1]:
              copy_ls_self.remove(soi_type_and_pos[b])

  return copy_ls_self, copy_ls_enemy, scout_die_between
        
#------------------------------------------------------------------------
#check the input whether is integer
def is_int(user_input_ls):
  try:
    for i in range(len(user_input_ls)):
      user_input_ls[i] = int(user_input_ls[i])
  except ValueError:
    return False
  else:
    return True
   
#------------------------------------------------------------------------
#check the scout die between
def scout_die(start_move, end_move, army_name, soi_type_and_pos, soi_type_and_pos_enemy, resources_ls):
  between_move = ''
  copy_ls_self = soi_type_and_pos[:]
  copy_ls_enemy = soi_type_and_pos_enemy[:]
  scout_die_between = False

  if abs(start_move[0] - end_move[0]) == 2:
    between_move = (min(start_move[0], end_move[0]) + 1 , start_move[1])
  elif abs(start_move[1] - end_move[1]) == 2:
    between_move = (start_move[0] , min(start_move[1], end_move[1]) + 1)

  for i in range(len(soi_type_and_pos_enemy)):
    if between_move == soi_type_and_pos_enemy[i][1]:
      scout_die_between = True 
  for a in range(len(resources_ls[0])):
    if between_move == resources_ls[0][a]:
      scout_die_between = True
  return scout_die_between

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Usage: python3 little_battle.py <filepath>")
    sys.exit()
  try:
    load_config_file(sys.argv[1])
  except SyntaxError as e:
    print(e)
    exit()
  except ArithmeticError as e:
    print(e)
    exit()
  except ValueError as e:
    print(e)
    exit()
  width, height, waters, woods, foods, golds, bases, resources_ls= load_infomation(sys.argv[1])

#Step 1: print the file is loaded
  print(f'Configuration file {sys.argv[1]} was loaded.')

#Step 2: print the 'start' information
  print('Game Started: Little Battle! (enter QUIT to quit the game)\n')

#Step 3: display the map
  re_total_ls, second_l, first_l = find_origin_lines(width, height)
  width_re_ls, height_re_ls, symbol = resources_pos_symbol(waters, waters, woods, foods, golds)
  re_total_ls = map_with_re_lines(re_total_ls, width_re_ls, height_re_ls, symbol)
  width_re_ls, height_re_ls, symbol = resources_pos_symbol(woods, waters, woods, foods, golds)
  re_total_ls = map_with_re_lines(re_total_ls, width_re_ls, height_re_ls, symbol)
  width_re_ls, height_re_ls, symbol = resources_pos_symbol(foods, waters, woods, foods, golds)
  re_total_ls = map_with_re_lines(re_total_ls, width_re_ls, height_re_ls, symbol)
  width_re_ls, height_re_ls, symbol = resources_pos_symbol(golds, waters, woods, foods, golds)
  re_total_ls = map_with_re_lines(re_total_ls, width_re_ls, height_re_ls, symbol)
  origin_map_ls = map_origin(re_total_ls, second_l)
  map_without_any_ls = map_without_any(width,height)
  print('(enter DIS to display the map)\n')

#Step 4: print the prices
  PRIS()
  print('(enter PRIS to display the price list)\n')

#Step 5:  
  map_ls = []
  while True:
    player, resources_hold, soi_type_and_pos, next_to_base, soi_type_and_pos_enemy, base, base_enemy = difference_player(player, width, height)
    
#5 - a/b:
    print_year_stage(now_year, player)

#5 - c:
    asset_resources(resources_hold)
#5 - d:
    while True:
      is_enough = check_resources_places(resources_hold)
      all_four_pos_occupied = check_next_to_base_occupied(next_to_base, soi_type_and_pos, soi_type_and_pos_enemy)

      if is_enough == False:
        break

      elif all_four_pos_occupied == True:
        break

      else:
        print('')
        army_typein = input('Which type of army to recruit, (enter) ‘S’, ‘A’, ‘K’, or ‘T’? Enter ‘NO’ to end this stage.\n')

#5 - d - iii (edge cases 2/3/4/5)
        if army_typein == 'QUIT':
          QUIT()
        elif army_typein == 'PRIS':
          PRIS()  
          continue
        elif army_typein == 'DIS':
          print('Please check the battlefield, commander.')
          print(first_l)
          print(second_l)
          map_ls = apply_position(map_without_any_ls, soi_type_and_pos, player, resources_ls)
          map_ls = map_origin(map_ls, second_l)
          continue
        elif army_typein == 'NO':
          break

#5 - d - ii (negative cases)
        elif army_typein not in ['S', 'A', 'K', 'T']:
          print('Sorry, invalid input. Try again.')
          continue

#5 - d - i (positive cases)
        elif army_typein in ['S', 'A', 'K', 'T']:
          army_ls = match_army(army_typein)
          recruit_enough = enough_to_recruit(resources_hold, army_ls)

#5 - d - iii (edge cases 1)
          if recruit_enough == False:
            continue

          while True:
            army_placein = input(f'\nYou want to recruit a {army_ls[0]}. Enter two integers as format ‘x y’ to place your army.\n')
                                    
#5 - d - i -3 (b/c/d)
            if army_placein == 'QUIT':
              exit()
            elif army_placein == 'PRIS':
              PRIS()  
              continue
            elif army_placein == 'DIS':
              print('Please check the battlefield, commander.')
              print(first_l)
              print(second_l)
              map_ls = apply_position(map_without_any_ls, soi_type_and_pos, player, resources_ls)
              map_ls = map_origin(map_ls, second_l)
              continue
              
#5 - d - i - 2 (negative cases)
            else:
              if army_placein == '':
                print('Sorry, invalid input. Try again.')
                continue
              else:
                army_placein_ls = army_placein.split(' ')
                if len(army_placein_ls) != 2:
                  print('Sorry, invalid input. Try again.')
                  continue
                elif is_int(army_placein_ls) != True:                    
                  print('Sorry, invalid input. Try again.')
                  continue
              
#5 - d - i- 3 (a)
                posin_vaild = check_posin(army_placein_ls, soi_type_and_pos, next_to_base, soi_type_and_pos_enemy)
                if posin_vaild == False:
                  continue

#5 -d - i - 1 (positive cases)
                else:

#5 - d - i - 1 - a
                  resources_hold = apply_cost(resources_hold, army_ls)
                  soi_type_and_pos = record_pos_type(army_ls, army_placein_ls, soi_type_and_pos)
                  map_ls = apply_position(map_without_any_ls, soi_type_and_pos, player, resources_ls)

#5 - d - i - 1 - b/c
                  print('')
                  print(f'You has recruited a {army_ls[0]}.\n')
                  asset_resources(resources_hold)
                  break
          continue
        break

#5 - e
    print(f"\n===Player {player}'s Stage: Move Armies===")

#5 - f
    no_army_this_round = False
    one_round_armies = soi_type_and_pos
    while True:
      if len(soi_type_and_pos) == 0 or no_army_this_round == True:
        print('')
        print('No Army to Move: next turn.\n')
        break
      else:
        print('')
        one_round_armies = print_armies(one_round_armies)
        print('')

#5 - g
        army_movein = input('Enter four integers as a format ‘x0 y0 x1 y1’ to represent move unit from (x0, y0) to (x1, y1) or ‘NO’ to end this turn.\n')
        
#5 - g - iii (edge cases 1/2/3/4)
        if army_movein == 'NO':
          print('')
          break
        elif army_movein == 'DIS':
          print('Please check the battlefield, commander.')
          print(first_l)
          print(second_l)
          map_ls = apply_position(map_without_any_ls, soi_type_and_pos, player, resources_ls)
          map_ls = map_origin(map_ls, second_l)
          continue
        elif army_movein == 'PRIS':
          PRIS()
          continue
        elif army_movein == 'QUIT':
          exit()

#5 - g - ii (negative cases)
        #input is not integers
        else:
          if army_movein == '':
            print('Invalid move. Try again.')
            continue
          else:
            army_movein_ls = army_movein.split(' ')
            if len(army_movein_ls) != 4:
              print('Invalid move. Try again.')
              continue
            else:
                if is_int(army_movein_ls) != True:
                  print('Invalid move. Try again.')
                  continue
            
#5 - g - i - 1 (positive cases)
            start_move, end_move = start_end_pos(army_movein_ls)

#5 - g - i - 2 (negative cases - behave as Move results)
            correct_direction = limit_direction(start_move, end_move)
            if correct_direction == False:
              print('Invalid move. Try again.')
              continue

            correct_step = limit_one_step(start_move, end_move, soi_type_and_pos)
            if correct_step == False:
              print('Invalid move. Try again.')
              continue

#5 -g -i - 1 - ii (negative cases - behave as Move results)
            #c: (x0,y0) = (x1,y1)
            if start_move == end_move:
              print('Invalid move. Try again.')
              continue

            #b: (x,y) outside of the game map (bigger)
            if start_move[0] > width - 1 or start_move[1] > height - 1 or end_move[0] > width - 1 or end_move[1] > height -1:
              print('Invalid move. Try again.')
              continue
            #b: (x,y) outside of the game map (smaller)
            if start_move[0] < 0 or start_move[1] < 0 or end_move[0] < 0 or end_move[1] < 0:
              print('Invalid move. Try again.')
              continue            
            #a:
            have_other_armies = check_other_armies(end_move, soi_type_and_pos, base)
            if have_other_armies == True:
              print('Invalid move. Try again.')
              continue

#5 - g - i - 2 (positive cases - behave as Move results)
#b: Restrict a army can only walk once per turn (user input have moved once)           
            this_round_can_move = False
            for aa in range(len(one_round_armies)):
              if start_move in one_round_armies[aa]:
                this_round_can_move = True
            if this_round_can_move == False:
              print('Invalid move. Try again.') 
              continue

#positive cases (army have move):
            soi_type_and_pos, army_name, one_round_armies = army_will_move(start_move, end_move, soi_type_and_pos, one_round_armies)
            print(f'\nYou have moved {army_name} from {start_move} to {end_move}.')

#check the scout whether die between
            scout_die_between = scout_die(start_move, end_move, army_name, soi_type_and_pos, soi_type_and_pos_enemy, resources_ls)

#f: move to a resource
            resources_ls, resources_hold = move_to_resource(start_move, end_move, resources_ls, resources_hold, scout_die_between)

#g: the scout destroyed by something
            soi_type_and_pos, soi_type_and_pos_enemy, scout_die_between = destroy_scout(start_move, end_move, army_name, soi_type_and_pos, soi_type_and_pos_enemy, scout_die_between)

#c: move to the water
            soi_type_and_pos, soi_type_and_pos_enemy, scout_die_between = move_to_water(start_move, end_move, resources_ls, soi_type_and_pos, soi_type_and_pos_enemy, scout_die_between)
            
#c: move to a counter enemy (self army disappear)
            soi_type_and_pos, soi_type_and_pos_enemy = move_to_be_killed_army(player, end_move, army_name, soi_type_and_pos, soi_type_and_pos_enemy)

#d: move to the same type of army
            soi_type_and_pos, soi_type_and_pos_enemy = move_to_same_type_army(player, end_move, army_name, soi_type_and_pos, soi_type_and_pos_enemy)

#e: move to a counter enemy (enemy disappear)
            soi_type_and_pos, soi_type_and_pos_enemy = move_to_kill_other_army(player, end_move, army_name, soi_type_and_pos, soi_type_and_pos_enemy)

#h: win the game
            win_game(player, end_move, army_name, now_year, scout_die_between, base_enemy)
#----------------------------------------------
            if player == 1:
              soi_type_and_pos_1, soi_type_and_pos_2= soi_type_and_pos, soi_type_and_pos_enemy
            else:
              soi_type_and_pos_1, soi_type_and_pos_2 = soi_type_and_pos_enemy, soi_type_and_pos

#b: Restrict a army can only walk once per turn (No army can move)           
            if len(one_round_armies) == 0:
              no_army_this_round = True
              print('\nNo Army to Move: next turn.\n')
              map_ls = apply_position(map_without_any_ls, soi_type_and_pos, player, resources_ls)
              break        
            else:
              continue

#GO BACK
    if player == 2:
      now_year += 1
      player = 1
    elif player == 1:
      player = 2
    