import unittest
import pdb

from engine.ui.game_info import GameInfo
from engine.players.mock_player import MockPlayer
from engine.ui.pot import Pot
from engine.ui.board import Board
from nose.tools import *
from engine.ui.table import Table
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
        p[0].set_action(["CALL:10","RAISE:30"])
        p[1].set_action(["CALL:10","FOLD:0"])
        p[2].set_action(["FOLD:0"])
        tb.players = p
        tb.init_round()
        tb.preflop() # pid(3) -> pid(1)
        eq_(90, p[0].stack)
        eq_(190, p[1].stack)
        eq_(300, p[2].stack)
        eq_(1, len(tb.deactive))
        tb.street(GameInfo.FLOP)   # pid(1) -> pid(2)
        eq_(60, p[0].stack)
        eq_(190, p[1].stack)
        eq_(300, p[2].stack)
        eq_(2, len(tb.deactive))

    def test_to_turn(self):
        tb = Table()
        p = [MockPlayer(1,"a",100),MockPlayer(2,"b",200),MockPlayer(3,"c",300)]
        tb.setup(p, 5)
        p = [MockPlayer(1,"bb",100),MockPlayer(2,"n",200),MockPlayer(3,"sb",300)]
        p[0].set_action(["CALL:10","FOLD:0"])
        p[1].set_action(["RAISE:10","RAISE:20","RAISE:20"])
        p[2].set_action(["CALL:10","RAISE:10","CALL:20","RAISE:10","CALL:20"])
        for i in range(3): p[i].D = True
        tb.players = p
        tb.init_round()
        tb.sb_pos = 2
        tb.preflop()
        eq_(30,tb.pot.get_chip())
        tb.street(GameInfo.FLOP)
        eq_(70,tb.pot.get_chip())
        tb.street(GameInfo.FLOP)
        eq_(110,tb.pot.get_chip())
        eq_(90, p[0].stack)
        eq_(150, p[1].stack)
        eq_(250, p[2].stack)

        tb = Table()
        p = [MockPlayer(1,"a",100),MockPlayer(2,"b",200),MockPlayer(3,"c",300)]
        tb.setup(p, 5)
        p = [MockPlayer(1,"bb",100),MockPlayer(2,"n",200),MockPlayer(3,"sb",300)]
        p[0].set_action(["CALL:10","CALL:10","CALL:20","ALLIN:70"])
        p[1].set_action(["RAISE:10","RAISE:20","FOLD:0"])
        p[2].set_action(["CALL:10","RAISE:10","CALL:20","RAISE:10","CALL:70"])
        # for i in range(3): p[i].D = True
        tb.players = p
        tb.init_round()
        tb.sb_pos = 2
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
        p[0].set_action(["CALL:10","CHECK:0","RAISE:20","RAISE:10"])
        p[1].set_action(["RAISE:10","CHECK:0","CALL:20","CALL:10"])
        p[2].set_action(["CALL:10","CHECK:0","RAISE:10","FOLD:0"])
        tb.players = p
        tb.init_round()
        tb.sb_pos = 2
        tb.preflop()
        tb.street(GameInfo.FLOP)
        tb.street(GameInfo.TURN)
        tb.street(GameInfo.RIVER)
        eq_(60, p[0].stack)
        eq_(160, p[1].stack)
        eq_(280, p[2].stack)
        eq_(1,len(tb.deactive))
        eq_(0,len(tb.allin))

    def test_round(self):
        tb = Table()
        p = [MockPlayer(1,"sb",100),MockPlayer(2,"bb",200),MockPlayer(3,"n",300)]
        tb.setup(p, 5)
        p = [MockPlayer(1,"sb",100),MockPlayer(2,"bb",200),MockPlayer(3,"n",300)]
        p[0].set_action(["CALL:10","CHECK:0","RAISE:20","CALL:30","RAISE:20"])
        p[1].set_action(["CALL:10","CHECK:0","CALL:20","FOLD:0"])
        p[2].set_action(["RAISE:10","CHECK:0","RAISE:30","FOLD:0"])
        tb.players = p
        tb.init_round()
        tb.preflop()
        tb.street(GameInfo.FLOP)
        tb.street(GameInfo.TURN)
        tb.street(GameInfo.RIVER)
        eq_(130, tb.pot.get_chip())
        tb.showoff()
        eq_(100-60+130, p[0].getStack())
        eq_(200-30, p[1].getStack())
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
        tb.play_round()
        eq_(100-5, p[0].getStack())
        eq_(200-10+15, p[1].getStack())
        eq_(300, p[2].getStack())


if __name__ == '__main__':
    unittest.main()

