import subprocess
import random

from engine.ui.dealer import Dealer
from engine.ui.game_info import GameInfo
from engine.ui.board import Board
from engine.ui.deck import Deck
from engine.ui.pot import Pot
from engine.ui.hand_evaluator import HandEvaluator

class Table(object):

    def __init__(self):
        self.AUTO = True
        self.players = None
        self.sb_chip = None
        self.sb_pos = None
        self.round_count = 0
        self.retire = []  # who lost all money
        self.deactive = []  # who foled the round
        self.allin = []  # who did all-in in the round

        self.D = Dealer()
        self.E = HandEvaluator()
        self.deck = Deck()
        self.board = Board()
        self.pot = Pot()

    # You need to call this method before start the game.
    def setup(self, players, sb_chip):
        random.shuffle(players)
        self.players = players
        self.sb_pos = len(players)-1   # for init_round
        self.sb_chip = sb_chip
    
    # You need to call this method every time new round starts
    def init_round(self):
        self.round_count += 1
        self.board.reset()
        self.pot.reset()
        self.deck.recombine()
        self.sb_pos = (self.sb_pos+1)%len(self.players)
        self.allin = []
        self.deactive = []
        self.deactive += self.retire

    # public method to start the poker game
    def start_game(self, n):
        # Play round n times
        for i in range(n):
            # if one player beats the others then finish the game.
            if len(self.retire)+1 == len(self.players): break
            self.play_round()
    
    # play one round
    def play_round(self):
        if not self.AUTO: subprocess.call('clear')

        self.init_round()
        self.preflop()
        if len(self.deactive)+1 != len(self.players): self.street(GameInfo.FLOP)
        if len(self.deactive)+1 != len(self.players): self.street(GameInfo.TURN)
        if len(self.deactive)+1 != len(self.players): self.street(GameInfo.RIVER)
        self.showoff()

        if not self.AUTO:
            print '\n> Enter any input to start next round ...\n'
            raw_input()

    def preflop(self):
        """ Preflop task
            1. collect blind
            2. change order of player (big blind is last player in pre-flop)
            3. ask action to players
        """
        self.D.collect_blind(self.pot, self.players, self.sb_pos, self.sb_chip)
        n = len(self.players)
        order = [(self.sb_pos+2+i)%n for i in range(n)]
        info = GameInfo(GameInfo.PREFLOP, self.sb_pos, self.players, self.pot, self.board, self.deactive, [])
        self.D.ask_action(self.players, self.pot, self.deactive, self.allin, order, info)

    def street(self, street):
        """ FLOP, TURN, RIVER task is almost the same
            1. reset bet (again starts from CHECK:0,FOLD,RAISE:10)
            2. add cards on board
            3. change order of player to sb -> bb -> ...
            4. ask action
        """
        self.pot.reset_bet()
        if street == GameInfo.FLOP:  # draw 3 cards in FLOP
            self.board.addCards(self.deck.drawCards(3))
        else:
            self.board.addCard(self.deck.drawCard())
        if not self.AUTO: self.board.display()

        # the case when left player is allin and call or
        #   the case when all player allin
        if len(self.deactive)+len(self.allin)+1 == len(self.players) or \
                len(self.deactive)+len(self.allin) == len(self.players):
            return

        # ask action to player
        n = len(self.players)
        order = [(self.sb_pos+i)%n for i in range(n)]
        info = GameInfo(street, self.sb_pos, self.players, self.pot, self.board, self.deactive, [])
        self.D.ask_action(self.players, self.pot, self.deactive, self.allin, order, info)

    def showoff(self):
        winner, result = self.D.check_winner(self.players, self.deactive, self.board)
        self.D.money_to_winner(self.pot, self.players, winner, self.allin)
        self.D.display_result(self.round_count, winner, result)
