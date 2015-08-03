import unittest
import pdb

from engine.ui.game_info import GameInfo
from engine.players.mock_player import MockPlayer
from engine.ui.pot import Pot
from engine.ui.board import Board
from nose.tools import *

class MockPTest(unittest.TestCase):

    def test_action(self):
        p = MockPlayer(1,'a',1000)
        p.set_action(["CALL:10","RAISE:20","FOLD:0"])
        ans = ["CALL:10","RAISE:20","FOLD:0"]
        for i in range(3):
            eq_(ans[i], p.action(None))

if __name__ == '__main__':
    unittest.main()
