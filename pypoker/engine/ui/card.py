import pdb
class Card:
    """
        Attributes
            rank: rank 2~A is coverted into 2~14. (Ace is treated as 14)
            suit: suit is defined as integer constant (See below)
    """
    CLUB = 2
    DIAMOND = 4
    HEART = 8
    SPADE = 16
    RANK_MAP = {2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9', 10:'T', 11:'J', 12:'Q', 13:'K',14:'A'}
    SUIT_MAP = {CLUB:'C', DIAMOND:'D', HEART:'H', SPADE:'S'}

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def getRank(self): return self.rank

    def getSuit(self): return self.suit

    def getRankStr(self): return self.RANK_MAP[self.rank]

    def getSuitStr(self): return self.SUIT_MAP[self.suit]

    # Card(1, 4).toString() => AD
    def toString(self): return self.RANK_MAP[self.rank] + self.SUIT_MAP[self.suit]

    # Card(1, 4).toString2() => Ad
    def toString2(self): return self.RANK_MAP[self.rank] + self.SUIT_MAP[self.suit].lower()

    def toID(self):
        """Computes card id which is defined by its rank and suit
            
            Use this id to identify Card instances are same card or not.

            Returns:
                id: ID of the card
                ex.) rank:2, suit:C => 2
                     rank:2, suit:D => 15
                     rank:3, suit:D => 16
        """
        rank = 1 if self.rank==14 else self.rank
        temp = self.suit>>1
        num = 0
        while not temp&1:
            num += 1
            temp >>=1
        return rank+13*num
