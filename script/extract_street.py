# add path to the data directory to read file
import os
import sys
cwd = os.path.realpath(__file__)
path_to_data = cwd[:-len("script/extract_street.py")]+"data/"

import pdb
import re
import csv
import data_processor
def extractStreetData(data, key):
  chunk = []
  for d in data:
    if key in d:
      chunk.append(d[key])
  return chunk

def streetToCSV(data, key):
  chunk = []
  for one_game in data:
    for i in range(len(one_game)):
      if i==0 and key!='PREFLOP': continue
      tmp = [None for j in range(2)]
      d = one_game[i]
      tmp[0] = d[0]
      if d[1][0] == 'F':
        tmp[1] = 'FOLDS'
      elif d[1][:5] == 'Raise':
        tmp[1] = 'RAISE'
      elif d[1][:2] == 'Ca':
        tmp[1] = 'CALL'
      elif d[1][:2] == 'Ch':
        tmp[1] = 'CHECKS'
      elif d[1][0] == 'A':
        tmp[1] = 'ALLIN'
      elif d[1][0] == 'B':
        tmp[1] = 'BETS'
      else:
        continue
      chunk.append(tmp)
  # write to csv
  with open(path_to_data+'csv/'+key+'.csv', 'a') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerows(chunk)
  print key+' DONE'


def main():
  formatter = data_processor.Formatter()
  data = formatter.format(path_to_data+"text/in.txt")
  streetToCSV(extractStreetData(data, 'PREFLOP'),'PREFLOP')
  streetToCSV(extractStreetData(data, 'FLOP'),'FLOP')
  streetToCSV(extractStreetData(data, 'TURN'),'TURN')
  streetToCSV(extractStreetData(data, 'RIVER'),'RIVER')

if __name__ == '__main__':
  main()
