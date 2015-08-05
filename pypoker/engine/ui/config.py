from engine.players.base_player import BasePlayer
from engine.players.human import Human

class Config:
    """
        This class reads game settings from config.txt
    """

    def __init__(self):
        self.data = {}

    def read(self, f_path):
        with open(f_path) as f:
            for line in f:
                line = line.rstrip('\n')
                if len(line)>0 and line[0]!='#':
                    key, val = line.split(':')
                    self.data[key] = val
        self.formatData(self.data)

    def formatData(self, data):
        data['sb_num'] = int(data['sb_num'])
        data['start_stack'] = int(data['start_stack'])
        data['round_num'] = int(data['round_num'])
        data['player_num'] = int(data['player_num'])

    def getPlayers(self):
        players = [None]*3
        stack = self.data['start_stack']
        for i in range(1,self.getPlayerNum()+1):
            name = self.data['p'+str(i)+'_name']
            strategy = self.data['p'+str(i)+'_strategy']
            players[i-1] = self.createPlayer(i, strategy, name, stack)
        return players

    def createPlayer(self, pid, strategy, name, stack):
        if strategy == 'human':
            return Human(pid, name, stack)
        if strategy == 'base':
            return BasePlayer(pid, name, stack)

    def getPlayerNum(self):
        return self.data['player_num']

    def getRoundNum(self):
        return self.data['round_num']

    def getSBChip(self):
        return self.data['sb_num']
