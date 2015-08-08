class BasePlayer(object):
    '''
        
        Player strategy is defined in action method.
        (So poker ai behavior depends on action method.)
    
        Attributes:
            NAME: the name of this player
            stack: start stack size of this player
            cards: hole card of this player

    '''
    
    def __init__(self, pid, player_name, start_stack):
        self.NAME = player_name
        self.pid = pid
        self.stack = start_stack
        self.cards = []

    def setHoleCards(self, cards):
        self.cards = cards

    def getName(self):
        return self.NAME

    def getStack(self):
        return self.stack

    def subStack(self, num):
        self.stack -= num

    def addStack(self, num):
        self.stack += num

    def getCards(self):
        return self.cards

    def action(self, info):
        return 'FOLD'   # This base class always folds the game.

    def cardsToString(self):
        """
        Returns:
            array of string of hole cards
        """
        s = []
        if len(self.cards) == 0:
            s.append('no cards')
        for card in self.cards:
            s.append(card.toString())
        return s
