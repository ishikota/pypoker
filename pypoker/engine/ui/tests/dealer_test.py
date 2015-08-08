import unittest
import pdb

from engine.ui.game_info import GameInfo
from engine.players.base_player import BasePlayer
from engine.players.mock_player import MockPlayer
from engine.ui.card import Card
from engine.ui.pot import Pot
from engine.ui.board import Board
from engine.ui.dealer import Dealer
from engine.ui.deck import Deck

from nose.tools import *

class MockLegalActPlayer(BasePlayer):

    def set_ans(self, ans):
        self.ans = ans

    def action(self, info):
        eq_(self.ans, info.get_legal_action())
        return info.get_legal_action()[1]


class DealerTest(unittest.TestCase):

    def setUp(self):
        players = [BasePlayer(1,"a",100),BasePlayer(2,"b",200)]
        pot = Pot()
        board = Board()
        self.INFO = GameInfo(-1, 0, players, pot, board, [], [])


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
        players = [MockPlayer(1,"a",100),MockPlayer(2,"b",200), MockPlayer(3,"c",10)]
        players[0].set_action(["RAISE:10","CALL:10"])
        players[1].set_action(["RAISE:20"])
        players[2].set_action(["ALLIN:10"])
        d.ask_action(players, pot, [], [], range(3),self.INFO)
        eq_(80,  players[0].stack)
        eq_(180,  players[1].stack)
        eq_(0,  players[2].stack)
        eq_(50, pot.chip)

        pot = Pot()
        players = [MockPlayer(1,"a",100),MockPlayer(2,"b",200), MockPlayer(3,"c",50)]
        players[0].set_action(["RAISE:10","FOLD:0"])
        players[1].set_action(["RAISE:20","RAISE:40"])
        players[2].set_action(["RAISE:30","CALL:40"])
        allin = []
        d.ask_action(players, pot, [], allin, range(3),self.INFO)
        eq_(90,  players[0].stack)
        eq_(140,  players[1].stack)
        eq_(0,  players[2].stack)
        eq_(120, pot.chip)
        eq_(players[2].pid, allin[0])

        pot = Pot()
        players = [MockPlayer(1,"a",100),MockPlayer(2,"b",15), MockPlayer(3,"c",50)]
        players[0].set_action(["RAISE:10","CALL:10"])
        players[1].set_action(["ALLIN:15"])
        players[2].set_action(["RAISE:20"])
        d.ask_action(players, pot, [], [], range(3),self.INFO)
        eq_(80,  players[0].stack)
        eq_(0,  players[1].stack)
        eq_(30,  players[2].stack)
        eq_(55, pot.chip)

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

    def test_legal_action_provide(self):
        self.INFO.street = GameInfo.PREFLOP
        self.INFO.sb_pos = 0
        d = Dealer()
        pot = Pot()
        pot.add(5); pot.add(10)  #
        players = [MockLegalActPlayer(1,"sb",100),MockLegalActPlayer(2,"bb",10)]
        players[0].set_ans(["FOLD:0","CALL:5","RAISE:15:15"])   # choose call
        players[1].set_ans(["FOLD:0","CALL:0", "RAISE:15:15"])
        d.ask_action(players, pot, [], [], range(2),self.INFO)

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
        pot.add(5) # sb bet
        pot.add(10) # bb bet
        acts = d.get_legal_action(player, pot, 10, 5)
        ok_("FOLD:0" in acts)
        ok_("CALL:5" in acts)
        ok_("RAISE:15:15" in acts)
        pot.add(15) # sb bet
        acts = d.get_legal_action(player, pot, 20, 10)
        ok_("FOLD:0" in acts)
        ok_("CALL:10" in acts)
        ok_("RAISE:20:20" in acts)
        pot.add(20) # bb bet
        acts = d.get_legal_action(player, pot, 30, 20)
        ok_("FOLD:0" in acts)
        ok_("CALL:10" in acts)
        ok_("RAISE:25:25" in acts)

    def test_correct_action(self):
        d = Dealer()
        player = BasePlayer(1,'a',100)
        pot = Pot()
        pot.add(5)  # sb
        pot.add(10)  # bb
        eq_('FOLD:0',d.correct_action(player, 'FOLD:10', pot, 10, 5))
        eq_('CALL:5',d.correct_action(player, 'CALL:5', pot, 10, 5))
        eq_('RAISE:15',d.correct_action(player, 'RAISE:15', pot, 10, 5))
        eq_('FOLD:0',d.correct_action(player, 'CALL:15', pot, 10, 5))
        eq_('FOLD:0',d.correct_action(player, 'RAISE:120', pot, 10, 0))
        pot.add(15)  # sb
        eq_('RAISE:20', d.correct_action(player, 'RAISE:20', pot, 20, 10))
        pot.add(20)  # bb
        eq_('CALL:10', d.correct_action(player, 'CALL:10',pot, 30, 20))

    def test_deal_card(self):
        d = Dealer()
        deck = Deck()
        players = [MockPlayer(1,"a",100-5),MockPlayer(2,"b",15), MockPlayer(3,"c",50)]
        d.deal_card(deck, players, [])
        eq_(2, players[0].getCards()[0].toID())
        eq_(15, players[0].getCards()[1].toID())
        eq_(28, players[1].getCards()[0].toID())
        eq_(41, players[1].getCards()[1].toID())
        eq_(3, players[2].getCards()[0].toID())
        eq_(16, players[2].getCards()[1].toID())

if __name__ == '__main__':
    unittest.main()

