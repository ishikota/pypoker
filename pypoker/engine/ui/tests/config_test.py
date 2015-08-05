import unittest
import pdb

from engine.ui.config import Config
from engine.players.base_player import BasePlayer
from engine.players.human import Human

from nose.tools import *

class ConfigTest(unittest.TestCase):

    def test_read():
        pass

    def test_read(self):
        name_len = len("config_test.py")
        if __file__[-1] == 'c': # if __file__ is config.pyc
            name_len += 1
        path_to_file = __file__[:-name_len]
        C = Config()
        C.read(path_to_file+"config.txt")
        eq_(10, C.getRoundNum())
        eq_(5, C.getSBChip())
        players = C.getPlayers()
        name_ans = ["base1 san", "human2 san"]
        class_ans = [BasePlayer, Human]
        for i in range(C.getPlayerNum()):
            player = players[i]
            eq_(name_ans[i], player.getName())
            eq_(200, player.getStack())
            ok_(isinstance(player, class_ans[i]))

if __name__ == '__main__':
    unittest.main()
