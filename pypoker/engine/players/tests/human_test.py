import unittest
import pdb

from engine.ui.game_info import GameInfo
from engine.players.human import Human
from engine.ui.pot import Pot
from engine.ui.board import Board
from nose.tools import *

import engine.players.human as h

class HumanPTest(unittest.TestCase):


    def test_action(self):
        """
            Action identifier is
                1: fold
                2: call
                3: raise
        """

        p = h.Human(1,'a',1000)
        pot = Pot()
        b = Board()
        info = GameInfo(GameInfo.PREFLOP,0,[p,p],pot,b,[],[])
        info.set_legal_action(["FOLD:0","CALL:10","RAISE:15:15"])

        # set mock raw_input
        def raw_input_mock():
            return "1"
        h.raw_input = raw_input_mock
        act = p.action(info)
        eq_("FOLD:0", act)

        def raw_input_mock():
            return "2"
        h.raw_input = raw_input_mock
        act = p.action(info)
        eq_("CALL:10", act)

        def raw_input_mock():
            return "3"
        h.raw_input = raw_input_mock
        act = p.action(info)
        eq_("RAISE:3", act)     # this player all ways type 3

if __name__ == '__main__':
    unittest.main()
