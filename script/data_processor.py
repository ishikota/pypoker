import pdb
import re
import csv

class Formatter:
  """
  Extract each game data from original data and formats it.
  Top level function is format method.
  This method do these things.
  - devide the src text data into each game
  - extract defined information from each game and replace it.
  - returns formatted game data.
  """


  def format(self, f_name):
    """
    API to devide game data into each game data and format it.
    
    Args:
      f_name: file name of original game data
    
    Returns:
      formatted game data devided by each game.
    """
    f = open(f_name)
    data = f.readlines()
    f.close()
    data = self.devideDataByGame(data)
    N = len(data)
    result = []
    for i in range(N):
      result.append(self.extractGameData(data[i]))
    return result

  def devideDataByGame(self, data):
    N = len(data)
    memo_index = 0
    memo = [[]]
    cp = 0
    while cp < N:
      if data[cp] == '\r\n':  # Each game data is devided by 3 blank line.
        memo_index += 1
        memo.append([])
        while cp+1 < N and data[cp+1] == '\r\n':
          cp += 1
      else:
        memo[memo_index].append(data[cp])
      cp += 1 
    memo.remove([])
    return memo

  def extractGameData(self, data):
    N = len(data)
    cp = 0
    res = {}
    while cp< N:
      memo = []
      if data[cp][:5] == 'Stage':
        cp, memo = self.extractStageInfo(data, cp)
        res['Stage'] = memo
      elif data[cp][:-2] == '*** POCKET CARDS ***':
        cp, memo = self.extractPocketCardsInfo(data, cp)
        res['PREFLOP'] = memo
      elif data[cp][:12] == '*** FLOP ***':
        cp, memo = self.extractFLOPInfo(data, cp)
        res['FLOP'] = memo
      elif data[cp][:12] == '*** TURN ***':
        cp, memo = self.extractFLOPInfo(data, cp)
        res['TURN'] = memo
      elif data[cp][:13] == '*** RIVER ***':
        cp, memo = self.extractFLOPInfo(data, cp)
        res['RIVER'] = memo
      elif data[cp][:-2] == '*** SHOW DOWN ***':
        cp, memo = self.extractShowDownInfo(data, cp)
        res['SHOWDOWN'] = memo
      elif data[cp][:-2] == '*** SUMMARY ***':
        cp, memo = self.extractSummary(data, cp)
        res['SUMMARY'] = memo
      else: # blind action
        cp += 1
    return res

  def extractStageInfo(self, data, cp):
    """
      Returns array of these data.
      1: game id
      2: player info => (seat, id, stack)
      3: blind info => ({sb, bb}, player id, bet amount)
    """
    memo = []
    while data[cp] != '*** POCKET CARDS ***\r\n':
      if data[cp][:5] == 'Stage':
        memo.append(self.extractStageID(data[cp]))
      elif data[cp][:5] == 'Table':
        pass
      elif data[cp][:4] == 'Seat':
        memo.append(self.extractPlayerData(data[cp]))
      else:
        info = self.extractBlindInfo(data[cp]) # may return None
        if info: memo.append(info)
      cp+=1
    return cp, memo

  def extractStageID(self, txt):
    p = r'#([0-9]+)'
    ob = re.search(p,txt)
    if ob:
      return ob.group(1)
  
  def extractPlayerData(self, txt):
    seat = self.extractPlayerSeat(txt)
    pid = self.extractPlayerID(txt)
    chip = self.extractChip(txt)
    return seat, pid, chip
  
  def extractPlayerSeat(self,txt):
    p = 'Seat ([0-9]+)'
    ob = re.search(p,txt)
    if ob: return ob.group(1)
  
  def extractPlayerID(self, txt):
    p = r'- ([0-9a-zA-Z/+]+)'
    ob = re.search(p,txt)
    if ob: return ob.group(1)
  
  def extractChip(self, txt):
    p = r'\$([0-9.]+)'
    ob = re.search(p,txt)
    if ob: return ob.group(1)

  def extractBlindInfo(self,txt):
    p = r'([0-9a-zA-Z/+]+) - Posts small blind \$([0-9]+)'
    ob = re.search(p,txt)
    if ob: return 'sb', ob.group(1), ob.group(2) # sb, pid, blind num
    p = r'([0-9a-zA-Z/+]+) - Posts big blind \$([0-9]+)'
    ob = re.search(p,txt)
    if ob: return 'bb', ob.group(1), ob.group(2) # bb, pid, blind num

  def extractBoardInfo(self, txt):
    p = r'([1-9TJQKA][hscd])'
    return re.findall(p,txt)

  def extractAction(self,txt):
    p = r'([a-zA-Z0-9/+]+) - (.*)\r'
    ob = re.search(p, txt)
    if ob:return ob.group(1), ob.group(2) # pid , action

  def extractPocketCardsInfo(self, data, cp):
    if data[cp][:3] == '***': cp+=1
    memo = []
    while data[cp][:3] != '***':
      memo.append(self.extractAction(data[cp]))
      cp += 1
    return cp, memo

  def extractFLOPInfo(self, data, cp):
    memo = []
    memo.append(self.extractBoardInfo(data[cp]))
    cp += 1
    while data[cp][:3] != '***':
      memo.append(self.extractAction(data[cp]))
      cp += 1
    return cp, memo

  def extractShowDownInfo(self, data, cp):
    memo = []
    cp += 1
    while data[cp][:3] != '***':
      memo.append(self.extractAction(data[cp]))
      cp += 1
    return cp, memo

  def extractSummaryData(self, txt):
    p = r'Seat ([0-9]+): ([a-zA-Z0-9]+) (.*)'
    ob = re.search(p, txt)
    if ob: return ob.group(1), ob.group(2), ob.group(3)

  def extractSummary(self, data, cp):
    memo = []
    cp += 1
    memo.append(self.extractChip(data[cp]))
    cp += 1
    memo.append(self.extractBoardInfo(data[cp]))
    while cp < len(data) and data[cp][0] != '':
      memo.append(self.extractSummaryData(data[cp]))
      cp+=1
    return cp,memo

