import unittest
import pdb

from engine.ui.game_info import GameInfo
from engine.players.mock_player import MockPlayer
from engine.ui.pot import Pot
from engine.ui.board import Board
from nose.tools import *
from engine.ui.table import Table
from engine.ui.card import Card
from engine.ui.debug_table import DebugTable

class TableTest(unittest.TestCase):


    def test_preflop(self):
        tb = Table()
        p = [MockPlayer(1,"a",100),MockPlayer(2,"b",200),MockPlayer(3,"c",300)]
        p[0].set_action(["FOLD:0"])
        p[1].set_action(["FOLD:0"])
        p[2].set_action(["FOLD:0"])
        tb.setup(p, 5)
        # to make the order player1(sb),2(bb),3
        p = [MockPlayer(1,"a",100),MockPlayer(2,"b",200),MockPlayer(3,"c",300)]
        p[0].set_action(["FOLD:0"])
        p[1].set_action(["FOLD:0"])
        p[2].set_action(["FOLD:0"])
        tb.players = p
        tb.init_round()
        tb.preflop()
        eq_(95, p[0].stack)
        eq_(190, p[1].stack)
        eq_(300, p[2].stack)
        eq_(15, tb.pot.chip)
        eq_(2, len(tb.deactive))

    def test_to_flop(self):
        tb = Table()
        p = [MockPlayer(1,"a",100),MockPlayer(2,"b",200),MockPlayer(3,"c",300)]
        tb.setup(p, 5)
        # to make the order player1(sb),2(bb),3
        p = [MockPlayer(1,"a",100),MockPlayer(2,"b",200),MockPlayer(3,"c",300)]
        p[0].set_action(["CALL:5","CALL:0", "FOLD:0"])
        p[1].set_action(["CALL:0","RAISE:10"])
        p[2].set_action(["FOLD:0"])
        tb.players = p
        tb.init_round()
        tb.preflop() # pid(3) -> pid(1)
        eq_(90, p[0].stack)
        eq_(190, p[1].stack)
        eq_(300, p[2].stack)
        eq_(1, len(tb.deactive))
        tb.street(GameInfo.FLOP)   # pid(1) -> pid(2)
        eq_(90, p[0].stack)
        eq_(180, p[1].stack)
        eq_(300, p[2].stack)
        eq_(2, len(tb.deactive))

    def test_to_turn(self):
        tb = Table()
        p = [MockPlayer(1,"a",100),MockPlayer(2,"b",200),MockPlayer(3,"c",300)]
        tb.setup(p, 5)
        p = [MockPlayer(1,"sb",100),MockPlayer(2,"bb",200),MockPlayer(3,"n",300)]
        p[0].set_action(["CALL:5","FOLD:0"])
        p[1].set_action(["CALL:0","RAISE:10","RAISE:10","RAISE:30"])
        p[2].set_action(["CALL:10","CALL:10","RAISE:20","CALL:20"])
        for i in range(3): p[i].D = True
        tb.players = p
        tb.init_round()
        tb.preflop()
        eq_(30,tb.pot.get_chip())
        tb.street(GameInfo.FLOP)
        eq_(50,tb.pot.get_chip())
        tb.street(GameInfo.TURN)
        eq_(130,tb.pot.get_chip())
        eq_(90, p[0].stack)
        eq_(140, p[1].stack)
        eq_(240, p[2].stack)

        tb = Table()
        p = [MockPlayer(1,"a",100),MockPlayer(2,"b",200),MockPlayer(3,"c",300)]
        tb.setup(p, 5)
        p = [MockPlayer(1,"bb",100),MockPlayer(2,"n",200),MockPlayer(3,"sb",300)]
        p[0].set_action(["CALL:5","RAISE:10","CALL:10","ALLIN:70"])
        p[1].set_action(["CALL:0","RAISE:20","FOLD:0"])
        p[2].set_action(["CALL:10","CALL:20","CALL:70"])
        # for i in range(3): p[i].D = True
        tb.players = p
        tb.init_round()
        tb.preflop()
        eq_(30,tb.pot.get_chip())
        tb.street(GameInfo.FLOP)
        eq_(90,tb.pot.get_chip())
        tb.street(GameInfo.TURN)
        eq_(230,tb.pot.get_chip())
        eq_(1,len(tb.allin))
        eq_(1,len(tb.deactive))

    def test_to_river(self):
        tb = Table()
        p = [MockPlayer(1,"a",100),MockPlayer(2,"b",200),MockPlayer(3,"c",300)]
        tb.setup(p, 5)
        p = [MockPlayer(1,"bb",100),MockPlayer(2,"n",200),MockPlayer(3,"sb",300)]
        p[0].set_action(["CALL:5","CHECK:0","RAISE:10","RAISE:10"])
        p[1].set_action(["CALL:0","CHECK:0","CALL:10","CALL:10"])
        p[2].set_action(["CALL:10","CHECK:0","CALL:10","FOLD:0"])
        tb.players = p
        tb.init_round()
        tb.preflop()
        tb.street(GameInfo.FLOP)
        tb.street(GameInfo.TURN)
        tb.street(GameInfo.RIVER)
        eq_(70, p[0].stack)
        eq_(170, p[1].stack)
        eq_(280, p[2].stack)
        eq_(1,len(tb.deactive))
        eq_(0,len(tb.allin))

    def test_round(self):
        tb = Table()
        p = [MockPlayer(1,"sb",100),MockPlayer(2,"bb",200),MockPlayer(3,"n",300)]
        tb.setup(p, 5)
        p = [MockPlayer(1,"sb",100),MockPlayer(2,"bb",200),MockPlayer(3,"n",300)]
        p[0].set_action(["CALL:5","CHECK:0","RAISE:10","CALL:20","CHECK:0","FOLD:0"])
        p[1].set_action(["CHECK:0","CHECK:0","RAISE:20","CALL:10","RAISE:10"])
        p[2].set_action(["CALL:10","CHECK:0","RAISE:30","FOLD:0"])
        tb.players = p
        tb.init_round()
        tb.preflop()
        tb.street(GameInfo.FLOP)
        tb.street(GameInfo.TURN)
        tb.street(GameInfo.RIVER)
        eq_(130, tb.pot.get_chip())
        tb.showoff()
        eq_(100-40, p[0].getStack())
        eq_(200-50+130, p[1].getStack())
        eq_(300-40,p[2].getStack())

    def test_blind(self):
        tb = Table()
        p = [MockPlayer(1,"sb",100),MockPlayer(2,"bb",200),MockPlayer(3,"n",300)]
        tb.setup(p, 5)
        p = [MockPlayer(1,"sb",100),MockPlayer(2,"bb",200),MockPlayer(3,"n",300)]
        p[0].set_action(["FOLD:0"])
        p[1].set_action(["FOLD:0"])
        p[2].set_action(["FOLD:0"])
        tb.players = p
        tb.init_round()
        tb.play_round()
        eq_(100-5, p[0].getStack())
        eq_(200-10+15, p[1].getStack())
        eq_(300, p[2].getStack())

    def test_skip_asking(self):
        """
            test 3 player game if last player is one player then jump to showoff
            Case1: ALLIN, FOLD, CALL -> do not ask action to left player
            Case2: FOLD, FOLD -> do not ask action to left player
        """
        tb = Table()
        p = [MockPlayer(1,"sb",100),MockPlayer(2,"bb",200),MockPlayer(3,"n",300)]
        tb.setup(p, 5)
        p = [MockPlayer(1,"sb",100),MockPlayer(2,"bb",200),MockPlayer(3,"n",5)]
        p[0].set_action(["FOLD:0"])
        p[1].set_action(["CHECK:0","FOLD:0"])   # this player is left player
        p[2].set_action(["CALL:10", "FOLD:0"])    # ALLIN:5, FOLD should not be called
        tb.players = p
        tb.init_round()
        tb.play_round()
        eq_(5,len(tb.board.cards))

        tb = Table()
        p = [MockPlayer(1,"sb",100),MockPlayer(2,"bb",200),MockPlayer(3,"n",300)]
        tb.setup(p, 5)
        p = [MockPlayer(1,"sb",100),MockPlayer(2,"bb",200),MockPlayer(3,"n",5)]
        p[0].set_action(["FOLD:0"])
        p[1].set_action(["FOLD:0"])   # this player is left player
        p[2].set_action(["FOLD:0"])
        tb.players = p
        tb.init_round()
        tb.play_round()
        eq_(0,len(tb.board.cards))
        eq_(205, p[1].stack)

    def test_retire(self):
        tb = DebugTable()
        p = [MockPlayer(1,"sb",100),MockPlayer(2,"bb",200),MockPlayer(3,"n",5)]
        tb.setup(p, 5)
        p = [MockPlayer(1,"sb",100),MockPlayer(2,"bb",200),MockPlayer(3,"n",5)]
        p[0].set_action(["CALL:5"])
        p[1].set_action(["FOLD:0"])
        p[2].set_action(["CALL:10"])  # ALLIN:5
        player_cards = [Card(14,2),Card(14,4),Card(8,2),Card(8,4),Card(4,2),Card(4,4)]
        board_cards = [Card(2,2),Card(2,4),Card(2,8),Card(2,16),Card(3,2)]
        tb.set_cheat_cards(player_cards, board_cards)
        tb.players = p
        tb.init_round()
        tb.play_round()
        eq_(115, p[0].stack)
        eq_(p[2].pid,tb.retire[0])

    def test_cheat_table(self):
        tb = DebugTable()
        p = [MockPlayer(1,"sb",100),MockPlayer(2,"bb",200),MockPlayer(3,"n",300)]
        tb.setup(p, 5)
        p = [MockPlayer(1,"sb",100),MockPlayer(2,"bb",200),MockPlayer(3,"n",300)]
        p[0].set_action(["CALL:5", "CHECK:0", "CHECK:0", "CHECK:0"])
        p[1].set_action(["CHECK:0", "CHECK:0", "CHECK:0", "CHECK:0"])
        p[2].set_action(["CALL:10", "CHECK:0", "CHECK:0", "CHECK:0"])
        player_cards = [Card(6,2),Card(6,4),Card(10,2),Card(8,4),Card(14,2),Card(11,4)]
        board_cards = [Card(2,2),Card(6,2),Card(8,8),Card(8,16),Card(12,2)]
        tb.set_cheat_cards(player_cards, board_cards)
        tb.players = p
        tb.init_round()
        tb.play_round()
        eq_(120,p[0].stack)

if __name__ == '__main__':
    unittest.main()

