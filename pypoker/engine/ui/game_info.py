class GameInfo:
    """ This object holds game information which is needed to think next hand.
    
    Attributes:
        street: current game street flg (PREFLOP=2, FLOP=4, TURN=8, RIVER=16)
        sb_pos: index of small blind player in players array
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
    

    def __init__(self, street, sb_pos, players, pot, board, deactive, last_actions):
        self.street = street
        self.sb_pos = sb_pos
        self.players = players
        self.pot = pot
        self.board = board
        self.player_stacks = self.get_player_stack(players)
        self.active_players = self.get_active_player(players, deactive)
        self.last_actions = last_actions
        self.legal_actions = None   # this info is set only when dealer asks action to player


    def display(self):
        """
            Display formatted game information on stdout.
        """
        div = '='*30
        print ''
        print div
        print ' STREET : '+self.STREET_MAP[self.street]
        print ' POT    : '+str(self.pot.get_chip())
        print ' BOARD  : '+self.board.toString()
        print ' STACK  : {0}'.format(self.get_player_stack4display())
        print ' ACTIVE : {0}'.format(self.get_active_player4display())
        print ' LAST ACTION: {0}'.format(self.get_last_acts4display())
        print div
        print ''

    def get_player_stack(self, players):
        """
            return all player's id and their stack in array
            format is [player_id:stack, player_id:stack, ...]
        """
        array = []
        for player in players:
            array.append(str(player.pid)+':'+str(player.getStack()))
        return array

    def get_active_player(self, players, deactive):
        """
        return active players in array
        format is [player_id, player_id, ...]
        """
        array = []
        for player in players:
            if player.pid not in deactive:
                array.append(player.pid)
        return array

    def get_last_acts(self):
        """
            return actions which played in this street
            format is [player_id:action,...]
        """
        array = []
        for action in self.last_actions:
            pid, act, num = action.split(':')
            array.append(':'.join([pid,act,num]))
        return array

    def get_player_stack4display(self):
        array = []
        for player in self.players:
            array.append("{0}:{1:d}".format(player.getName(),player.getStack()))
        return array
  
    def get_active_player4display(self):
        array = []
        for player in self.players:
            if player.pid in self.active_players:
                array.append(player.getName())
        return array

    def get_last_acts4display(self):
        name_map = {}
        for player in self.players:
            name_map[player.pid] = player.getName()
        array = []
        for action in self.last_actions:
            pid, act, num = action.split(':')
            name = name_map[int(pid)]
            array.append(':'.join([name,act,num]))
        return array

    def set_legal_action(self, actions):
        self.legal_actions = actions

    def get_legal_action(self):
        return self.legal_actions
