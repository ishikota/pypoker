# add path to the data directory to read file
import os
import sys
cwd = os.path.realpath(__file__)
path_to_data = cwd[:-len("script/extract_street.py")]+"data/"

import pdb
import re
import csv
import copy
import data_processor

# return list of
# [ player_id, [], [], stack, active_num]
def readPlayersInfo(stage_info):
  res = {}
  player_num = len(stage_info) -3 # game_id, sb_info, bb_info
  res['pot'] = 0
  res['actions'] = [0,0,0]
  res['active'] = player_num
  for item in stage_info:
    if isinstance(item, str) or item[0] == 'sb' or item[0] == 'bb':
      continue
    res[item[1]] = {'act':[], 'stack':float(item[2])}
  return res

def extractAction(act):
  if act[:4] == 'Fold': return 'Folds',0
  if act == 'Checks': return 'Checks', 0
  if act[:5] == 'Calls':
    ob = re.search('\$([0-9.]+)', act)
    return 'Calls', float(ob.group(1))
  if act[:6] == 'Raises':
    ob = re.search('\$([0-9.]+) to \$[0-9]+', act)
    if not ob: pdb.set_trace()
    return 'Raises', float(ob.group(1))
  if act[:4] == 'Bets':
    ob = re.search('\$([0-9.]+)', act)
    return 'Bets', float(ob.group(1))
  if act[:3] == 'All':
    ob = re.search('\$([0-9.]+)', act)
    return 'All-In', float(ob.group(1))

def readActions(p_dict, street_data):
  pot = p_dict['pot']
  act_index = {'Folds':0, 'Calls':1, 'Checks':1 ,'Raises':2, 'Bets':2, 'All-In':2}
  action_holder = p_dict['actions']
  for pid, act in street_data:
    if act[:8] == 'returned': continue
    if pid not in p_dict: continue
    action, chip = extractAction(act)
    d = ['?', [0,0,0], 0, p_dict[pid]['stack'], p_dict['active']]
    d[0] = action
    for i in range(3): d[1][i] = action_holder[i]
    d[2] = pot
    d[3] -= chip
    d[4] = p_dict['active']
    action_holder[act_index[action]] += 1
    if action == 'Folds': p_dict['active'] -=1
    if p_dict['active'] < 0 : pdb.set_trace()
    p_dict[pid]['act'].append(d)
    p_dict[pid]['stack'] = d[3]
    pot += chip
  p_dict['pot'] = pot

def toCSV(data, key):
  chunk = []
  for m in data:
    tmp = []
    tmp.append(m[0])
    tmp.append(m[1][0])
    tmp.append(m[1][1])
    tmp.append(m[1][2])
    tmp.append(m[2])
    tmp.append(m[3])
    tmp.append(m[4])
    chunk.append(tmp)
  # write to csv
  with open(path_to_data+'csv/'+key+'.csv', 'a') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(['action', 'FOLD','CALL/CHECK','BETS/RAISE',\
        'pot','stack','active player'])
    writer.writerows(chunk)
  print 'Writed to '+key+'.csv'

def main():
  formatter = data_processor.Formatter()
  data = formatter.format(path_to_data+"text/in.txt")
  res = {'PREFLOP':[],'FLOP':[],'TURN':[],'RIVER':[]}
  for game_data in data:
    # read preflopp actions
    pdb.set_trace()
    p_dict = readPlayersInfo(game_data['Stage'])
    readActions(p_dict, game_data['PREFLOP'])
    for key in p_dict:
      if key in ['pot','actions','active']: continue
      for act in p_dict[key]['act']:
        res['PREFLOP'].append(act)

    if 'FLOP' not in game_data: continue
    # reset player action history in p_dict
    p_dict2 = copy.deepcopy(p_dict)
    p_dict2['actions'] = [0,0,0]
    for key in p_dict2:
      if key in ['pot','actions','active']: continue
      p_dict2[key]['act'] = []
    # read FLOP actions
    readActions(p_dict2, game_data['FLOP'][1:]) # [1:] exclude board info
    for key in p_dict2:
      if key in ['pot','actions','active']: continue
      for act in p_dict2[key]['act']:
        res['FLOP'].append(act)


    if 'TURN' not in game_data:continue
    # reset player action history in p_dict
    p_dict3 = copy.deepcopy(p_dict2)
    p_dict3['actions'] = [0,0,0]
    for key in p_dict3:
      if key in ['pot','actions','active']: continue
      p_dict3[key]['act'] = []
    # read RIVER actions
    readActions(p_dict3, game_data['TURN'][1:]) # [1:] exclude board info
    for key in p_dict3:
      if key in ['pot','actions','active']: continue
      for act in p_dict3[key]['act']:
          res['TURN'].append(act)

    
    if 'RIVER' not in game_data:continue
    # reset player action history in p_dict
    p_dict4 = copy.deepcopy(p_dict3)
    p_dict4['actions'] = [0,0,0]
    for key in p_dict4:
      if key in ['pot','actions','active']: continue
      p_dict4[key]['act'] = []
    # read RIVER actions
    readActions(p_dict4, game_data['RIVER'][1:]) # [1:] exclude board info
    for key in p_dict4:
      if key in ['pot','actions','active']: continue
      for act in p_dict4[key]['act']:
          res['RIVER'].append(act)


  toCSV(res['PREFLOP'], 'action_preflop')
  toCSV(res['FLOP'], 'action_flop')
  toCSV(res['TURN'], 'action_turn')
  toCSV(res['RIVER'], 'action_river')


if __name__=='__main__':
  main()
