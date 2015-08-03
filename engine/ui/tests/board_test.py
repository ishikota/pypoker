import unittest
import pdb

from engine.ui.board import Board
from engine.ui.card import Card
class BoardTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_addCard(self):
        c1 = Card(3, Card.SPADE)
        c2 = Card(11, Card.HEART)
        b = Board()
        b.addCard(c1)
        b.addCard(c2)
        self.assertEqual(2, b.getNumCards())
        b.reset()
        self.assertEqual(0, b.getNumCards())

if __name__ == '__main__':
    unittest.main()
