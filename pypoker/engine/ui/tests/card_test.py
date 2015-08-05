import unittest
import pdb

from engine.ui.card import Card
import random

class CardTest(unittest.TestCase):

    def setUp(self):
        pass

    def testToString(self):
        temp = [Card.CLUB, Card.DIAMOND, Card.HEART, Card.SPADE]
        for i in range(500):
            rank = random.randint(2,14)
            ind = random.randint(0,3)
            suit = temp[ind]
            card = Card(rank, suit)
            ans_rank = str(rank) if 1<rank<10 else 'T' if rank==10 else 'J' if rank==11 else 'Q'\
            if rank==12 else 'K' if rank==13 else 'A'
            ans_suit = 'C' if ind==0 else 'D' if ind==1 else 'H' if ind==2 else 'S'
            self.assertEqual(ans_rank+ans_suit, card.toString())

    def testToString2(self):
        c = Card(12,4)
        self.assertEqual('Qd', c.toString2())

    def testToID(self):
        card = Card(3,8)
        self.assertEqual(29, card.toID())
        card = Card(1,16)
        self.assertEqual(40, card.toID())

if __name__ == '__main__':
    unittest.main()
