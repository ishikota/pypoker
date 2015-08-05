from engine.ui.table import Table
from engine.ui.deck import Deck
from engine.ui.game_info import GameInfo

class DebugTable(Table):
    """
        Replacement class of Table class for debug.
        This class overrides play_round method to 
        controll the player and board card in game.
        You can controll the cards in round by passing
        players and board cards in parameter.
    """
    """
    def __init__(self):
        super(DebugTable, self).__init__()
        self.player_cards = None
        self.board_cards = None
    """
    def set_cheat_cards(self, player_cards, board_cards):
        self.player_cards = player_cards
        self.board_cards = board_cards

    # You need to call this method every time new round starts
    def init_round(self):
        self.round_count += 1
        self.board.reset()
        self.pot.reset()
        self.deck = Deck() # every time use new deck
        self.cheat_shuffle(self.deck, self.player_cards, self.board_cards)
        self.D.deal_card(self.deck, self.players, self.retire)
        self.sb_pos = (self.sb_pos+1)%len(self.players)
        self.allin = []
        self.deactive = []
        self.deactive += self.retire

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

    def cheat_shuffle(self, deck, player_cards, board_cards):
        """ 
            Replaces the cards on top of the deck to passed cards
            (the cards on top of the deck is used in a next round.)

            Args:
                player_cards: array of hole cards for player.
                    [ [cards for players[0]], [cards for players[1]], ... ]
                board_cards: array of card. small index card is draw ealrier.
                    if board_cards =[ c1,c2,c3,c4,c5 ] then
                    => board of FLOP [c1,c2,c3]
                    => board of TURN [c1,c2,c3,c4]
                    => board of RIVER [c1,c2,c3,c4,c5]
        """
        i = 0
        for c in player_cards:
            deck.cards[i] = c
            i+=1
        for c in board_cards:
            deck.cards[i] = c
            i+=1
