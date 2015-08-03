import unittest
import pdb

from engine.ui.game_info import GameInfo
from engine.players.base_player import BasePlayer
from engine.ui.pot import Pot
from engine.ui.board import Board
from nose.tools import *

class GameInfoTest(unittest.TestCase):

    def get_info(self):
        players = []
        players.append(BasePlayer(1,"a",1000))
        players.append(BasePlayer(2,"b",1000))
        stage = GameInfo.PREFLOP
        pot = Pot()
        board = Board()
        stacks = [p.stack for p in players]
        active = [p.pid for p in players]
        histry = []
        return GameInfo(players,stage,pot,board,stacks,active,histry)

    def test_stack_info(self):
        G = self.get_info()
        ans = ["a:1000", "b:1000"]
        eq_(ans, G.get_stacks())

    def test_active_info(self):
        G = self.get_info()
        ans = ["a", "b"]
        eq_(ans, G.get_active())

    def test_history(self):
        G = self.get_info()
        G.last_actions = ["1:RAISE:50"]
        ans = ["a:RAISE:50"]
        eq_(ans, G.get_last_acts())

if __name__ == '__main__':
    unittest.main()
