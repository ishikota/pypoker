import random
from card import Card

class Deck:
    """First Deck object has 52 cards. (doesn't include joker)
        
        Attributes
            cards: array of un-used cards.(First, it has 52 card elements)
            used: array of drawn card.
    """
    def __init__(self):
        self.cards = []
        self.used = []
        for rank in range(2,15):
            for suit in [Card.CLUB, Card.DIAMOND, Card.HEART, Card.SPADE]:
                self.cards.append(Card(rank, suit))

    def shuffle(self, recombine):
        if recombine:
            self.recombine()
        random.shuffle(self.cards)
    
    def drawCard(self):
        card = self.cards.pop(0)
        self.used.append(card)
        return card

    def drawCards(self, num):
        array = [0] * num
        for i in range(num):
            array[i] = self.drawCard()
        return array
    
    def recombine(self):
        self.cards += self.used
        self.used = []
