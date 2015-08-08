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
        street = GameInfo.NEWGAME
        pot = Pot()
        board = Board()
        histry = []
        return GameInfo(street,0,players,pot,board,[],histry)

    def test_stack_info(self):
        G = self.get_info()
        eq_(["1:1000", "2:1000"], G.player_stacks)
        eq_(["a:1000", "b:1000"], G.get_player_stack4display())

    def test_active_info(self):
        G = self.get_info()
        eq_([1,2], G.active_players)
        eq_(["a", "b"], G.get_active_player4display())

    def test_history(self):
        G = self.get_info()
        G.last_actions = ["1:RAISE:50"]
        eq_(["1:RAISE:50"], G.get_last_acts())
        eq_(["a:RAISE:50"], G.get_last_acts4display())

if __name__ == '__main__':
    unittest.main()
