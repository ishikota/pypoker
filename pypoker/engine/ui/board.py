class Board:

  def __init__(self):
    # holds community card in this array
    self.cards = []

  def addCard(self, card):
    self.cards.append(card)

  def addCards(self, cards):
    self.cards += cards

  def getNumCards(self):
    return len(self.cards)

  def getCards(self):
    return self.cards

  def display(self):
    print self.toString()

  def toString(self):
    s = []
    if len(self.cards) == 0:
      s.append('no cards')
    for card in self.cards:
      s.append(card.toString())
    return str(s)

  def reset(self):
    self.cards = []
