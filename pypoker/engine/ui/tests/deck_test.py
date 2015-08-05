# test template
import unittest
import pdb

from engine.ui.deck import Deck
from engine.ui.card import Card
class DeckTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_init(self):
        d = Deck()
        for i in range(len(d.cards)):
            print d.cards[i].toString()

    def test_drawCard(self):
        d = Deck()
        c = d.drawCard()
        for card in d.cards:
            if card.rank == c.rank and card.suit == c.suit:
                self.fail()
        self.assertEqual(len(d.used), 1)
        
        if not(d.used[0].rank == c.rank and d.used[0].suit == c.suit):
            self.fail()

    def test_drawCards(self):
        d = Deck()
        cards = d.drawCards(2)
        for c in cards:
            for card in d.cards:
                if (card.rank == c.rank and card.suit == c.suit):
                    self.fail(c.toString()+','+card.toString())
        for used in d.used:
            self.assertTrue(used in cards)

    def test_recombine(self):
        d = Deck()
        d.drawCards(2)
        d.drawCard()
        d.recombine()
        self.assertEqual(len(d.cards), 52)
        self.assertEqual(len(d.used), 0)

if __name__ == '__main__':
    unittest.main()
