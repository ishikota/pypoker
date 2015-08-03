class GameInfo:
    """ This object holds game information which is needed to think next hand.
    
    Attributes:
        street: current game street flg (PREFLOP=2, FLOP=4, TURN=8, RIVER=16)
        players: array of player
        pot: current pot size
        board: current board instance which holds community card array
        deactive: players who dropped this game
        last_action: array of action of other player in this street.(the action before you)
    """
    NEWGAME = 0
    PREFLOP = 2
    FLOP = 4
    TURN = 8
    RIVER = 16
    STREET_MAP = {NEWGAME:'NEW-GAME',PREFLOP:"PRE-FLOP", FLOP:"FLOP", TURN:"TURN", RIVER:"RIVER"}


    def __init__(self, street, players, pot, board, deactive, last_actions):
        self.street = street
        self.players = players
        self.pot = pot
        self.board = board
        self.player_stacks = self.fetch_stacks(players)
        self.active_players = self.fetch_active(players, deactive)
        self.last_actions = last_actions
        self.sb = -1

    def fetch_stacks(self, players):
        """
        return format
        [player_id:stack, player_id:stack, ...]
        """
        array = []
        for player in players:
            array.append(str(player.pid)+':'+str(player.getStack()))
        return array

    def fetch_active(self, players, deactive):
        """
        return format
        [player_id, player_id, ...]
        """
        array = []
        for player in players:
            if player.pid not in deactive:
                array.append(player.pid)
        return array

    def display(self):
        """
            Display formatted game information on stdout.
        """
        div = '='*30
        print ''
        print div
        print ' STREET : '+self.STREET_MAP[self.street]
        print ' POT    : '+str(self.pot.getChipNum())
        print ' BOARD  : '+self.board.toString()
        print ' STACK  : '+self.createStackStr(self.players)
        print ' ACTIVE : '+self.createActiveStr(self.players, self.active_players)
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
