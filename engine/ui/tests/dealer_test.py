import unittest
import pdb

from engine.ui.game_info import GameInfo
from engine.players.base_player import BasePlayer
from engine.players.mock_player import MockPlayer
from engine.ui.pot import Pot
from engine.ui.board import Board
from engine.ui.dealer import Dealer

from nose.tools import *

class DealerTest(unittest.TestCase):

    def setUp(self):
        players = [BasePlayer(1,"a",100),BasePlayer(2,"b",200)]
        pot = Pot()
        board = Board()
        self.INFO = GameInfo(0, 0, players, pot, board, [], [])


    def test_collect_blind(self):
        d = Dealer()
        pot = Pot()
        players = [BasePlayer(1,"a",100),BasePlayer(2,"b",200)]
        d.collect_blind(pot, players, 0, 5)
        eq_(95, players[0].stack)
        eq_(190, players[1].stack)
        d.collect_blind(pot, players, 1, 5)
        eq_(85, players[0].stack)
        eq_(185, players[1].stack)
        eq_(30, pot.chip)

    def test_ask_action(self):
        d = Dealer()
        pot = Pot()
        players = [MockPlayer(1,"a",100),MockPlayer(2,"b",200), MockPlayer(3,"c",15)]
        players[0].set_action(["CALL:10","CALL:20"])
        players[1].set_action(["RAISE:20"])
        players[2].set_action(["ALLIN:15"])
        d.ask_action(players, pot, [], [], range(3),self.INFO)
        eq_(80,  players[0].stack)
        eq_(180,  players[1].stack)
        eq_(0,  players[2].stack)
        eq_(55, pot.chip)
        
        pot = Pot()
        players = [MockPlayer(1,"a",100),MockPlayer(2,"b",200), MockPlayer(3,"c",50)]
        players[0].set_action(["CALL:10","FOLD:0"])
        players[1].set_action(["RAISE:20","RAISE:40"])
        players[2].set_action(["RAISE:30","CALL:40"])
        d.ask_action(players, pot, [], [], range(3),self.INFO)
        eq_(90,  players[0].stack)
        eq_(160,  players[1].stack)
        eq_(10,  players[2].stack)
        eq_(90, pot.chip)

        pot = Pot()
        players = [MockPlayer(1,"a",100),MockPlayer(2,"b",15), MockPlayer(3,"c",50)]
        players[0].set_action(["CALL:10","CALL:30"])
        players[1].set_action(["ALLIN:15"])
        players[2].set_action(["RAISE:30"])
        d.ask_action(players, pot, [], [], range(3),self.INFO)
        eq_(70,  players[0].stack)
        eq_(0,  players[1].stack)
        eq_(20,  players[2].stack)
        eq_(75, pot.chip)

        # preflop case => Do not need to ask BB player if SB player called
        self.INFO.street = GameInfo.PREFLOP
        self.INFO.sb_pos = 0
        pot = Pot()
        players = [MockPlayer(1,"a",100-5),MockPlayer(2,"b",15), MockPlayer(3,"c",50)]
        players[0].set_action(["FOLD:0"])  # SB
        players[1].set_action(["ALLIN:15"])  # BB
        players[2].set_action(["FOLD:0"])
        d.ask_action(players, pot, [], [], [2,0,1],self.INFO)
        eq_(100-5,  players[0].stack)
        eq_(15,  players[1].stack)


if __name__ == '__main__':
    unittest.main()

