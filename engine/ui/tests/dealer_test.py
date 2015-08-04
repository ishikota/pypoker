import unittest
import pdb

from engine.ui.game_info import GameInfo
from engine.players.base_player import BasePlayer
from engine.players.mock_player import MockPlayer
from engine.ui.card import Card
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

    def test_check_winner(self):
        d = Dealer()
        board = Board()
        players = [MockPlayer(1,"a",100),MockPlayer(2,"b",15)]

        # Case1
        community = [Card(3,4),Card(5,4),Card(7,2),Card(6,4),Card(10,2)]
        hole1 = [Card(2,4),Card(9,2)] # no pair
        hole2 = [Card(3,4),Card(8,2)] # one pair
        board.addCards(community)
        players[0].setHoleCards(hole1)
        players[1].setHoleCards(hole2)
        deactive = []
        winner, result = d.check_winner(players, deactive, board)
        ok_(len(winner)==1 and winner[0]==players[1])
        print result
        # Case2
        board.reset()
        community = [Card(3,4),Card(3,4),Card(3,2),Card(6,4),Card(10,2)]
        hole1 = [Card(3,4),Card(9,2)] # four card
        hole2 = [Card(4,4),Card(6,2)] # full house
        hole3 = [Card(2,4),Card(8,2)] # three card
        board.addCards(community)
        players.append(MockPlayer(3,"c",200))
        players[0].setHoleCards(hole1)
        players[1].setHoleCards(hole2)
        players[2].setHoleCards(hole3)
        deactive = []
        winner, result = d.check_winner(players, deactive, board)
        ok_(len(winner)==1 and winner[0]==players[0])
        print result

        deactive = [players[0].pid]
        winner, result = d.check_winner(players, deactive, board)
        ok_(len(winner)==1 and winner[0]==players[1])
        print result

    def test_legal_action(self):
        d = Dealer()
        player = BasePlayer(1,'a',100)
        pot = Pot()
        pot.add(5)
        pot.add(10)
        acts = d.get_legal_action(player, pot, 10, 0)
        ok_("FOLD:0" in acts)
        ok_("CALL:10" in acts)
        ok_("RAISE:15:15" in acts)
        pot.add(15)
        acts = d.get_legal_action(player, pot, 15, 0)
        ok_("FOLD:0" in acts)
        ok_("CALL:15" in acts)
        ok_("RAISE:20:20" in acts)
        acts = d.get_legal_action(player, pot, 0, 0)
        ok_("FOLD:0" in acts)
        ok_("CHECK:0" in acts)
        ok_("RAISE:20:20" in acts)




if __name__ == '__main__':
    unittest.main()

