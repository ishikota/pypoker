class GameInfo:
    """ This object holds game information which is needed to think next hand.
    
    Attributes:
        players: array of player
        param stage: current game stage(PREFLOP=2, FLOP=4, TURN=8, RIVER=16)
        pot: current pot size
        board: current board instance which holds community card array
        player_stacks: array of stack of each player
        active_players: array of active player id
        last_action: array of action of other player in this stage.(the action before you)
    """
    NEWGAME = 0
    PREFLOP = 2
    FLOP = 4
    TURN = 8
    RIVER = 16
    STAGE_MAP = {NEWGAME:'NEW-GAME',PREFLOP:"PRE-FLOP", FLOP:"FLOP", TURN:"TURN", RIVER:"RIVER"}

    def __init__(self, players, stage, pot, board, player_stacks, active_players, last_actions):
        self.players = players
        self.stage = stage
        self.pot = pot
        self.board = board
        self.player_stacks = player_stacks
        self.active_players = active_players
        self.last_actions = last_actions
        self.sb = -1


    def display(self):
        """
            Display formatted game information on stdout.
        """
        div = '='*30
        print ''
        print div
        print ' STAGE : '+self.STAGE_MAP[self.stage]
        print ' POT   : '+str(self.pot.getChipNum())
        print ' BOARD : '+self.board.toString()
        print ' STACK : '+self.createStackStr(self.players)
        print ' ACTIVE: '+self.createActiveStr(self.players, self.active_players)
        print ' LAST ACTION: '+self.createLastActionStr(self.players, self.last_actions)
        print div
        print ''

    def get_stacks(self):
        array = []
        for player in self.players:
            array.append("{0}:{1:d}".format(player.getName(),player.getStack()))
        return array
  
    def get_active(self):
        array = []
        for player in self.players:
            if player.pid in self.active_players:
                array.append(player.getName())
        return array

    def get_last_acts(self):
        name_map = {}
        for player in self.players:
            name_map[player.pid] = player.getName()
        res = []
        for action in self.last_actions:
            pid, act, num = action.split(':')
            name = name_map[int(pid)]
            res.append(':'.join([name,act,num]))
        return res
