import unittest
import pdb

from engine.ui.game_info import GameInfo
from engine.players.base_player import BasePlayer
from engine.ui.pot import Pot
from engine.ui.board import Board
from nose.tools import *

class PotTest(unittest.TestCase):

    def test_min_raise(self):
        p = Pot()
        p.add(5) # sb
        p.add(10) # bb
        eq_(15, p.get_min_raise())
        p.add(15) # raise 15
        eq_(20 ,p.get_min_raise())


if __name__ == '__main__':
    unittest.main()
