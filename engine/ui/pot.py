class Pot:
    """
        This pot calculates raise chip by folowwing Fixed-limit Texas Holdem,
        which raise range is fixed to (last_bet + (last_bet - last2_bet) )
    """

    def __init__(self):
        self.chip = 0
        self.last_bet = 0
        self.last2_bet = 0

    def reset(self):
        """
            Use this method when new round starts
        """
        self.chip = 0
        self.last_bet = 0
        self.last2_bet = 0

    def reset_bet(self):
        """
            Use this method when new street starts.
            (because this method only reset bet range)
        """
        self.last_bet = 0
        self.last2_bet = 0

    def add(self, num):
        """
            append chip to pot and update last bet info
        """
        self.chip += num
        self.last2_bet = self.last_bet
        self.last_bet = num

    def get_chip(self):
        return self.chip

    # return last bet amount which is used for calculates chip amount to Call
    def get_last_bet(self):
        return self.last_bet

    # chip amout to raise
    def get_min_raise(self):
        return self.last_bet + (self.last_bet - self.last2_bet)

