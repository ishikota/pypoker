from engine.ui.hand_evaluator import HandEvaluator

class Dealer(object):
    
    # CONSTANTS
    SMALL_BLIND = 5

    def __init__(self):
        self.E = HandEvaluator()

    def deal_card(self, deck, players, retire):
        for i in range(len(players)):
            if i not in retire:
                players[i].setHoleCards(deck.drawCards(2))

    def collect_blind(self, pot, players, sb_pos, sb_chip):
        """

        Collect the blind from players
        If blind player doesn't have enough money the all-in.

        Args:
            pot: pot to add collected blind
            players: players who collect blind from
            sb_pos: index of small blind player in players
            sb_chip: amount of small blind
        """
        # collect small blind
        sb_player = players[sb_pos]
        chip = sb_player.getStack()
        chip = min(chip, sb_chip)
        pot.add(chip)
        sb_player.subStack(chip)
        # collect big blind
        bb_player = players[(sb_pos+1)%len(players)]
        chip = bb_player.getStack()
        chip = min(chip, sb_chip*2)
        pot.add(chip)
        bb_player.subStack(chip)

    def ask_action(self, players, pot, deactive, allin, order, info):
        """

        Ask action to passed players until all players action is fixed.

        Args:
            players: players to ask action
            deactive: pid of players who do not need to ask
            allin: pid of players who allin 
            order: ordered player index to ask action.
            info: current game information.
                  player use this info to decide his action.
        """
        i = 0
        n = len(order)
        pay = [0 for i2 in range(n)]

        # If current street is PREFLOP then BB player has fixed his action from first.
        is_preflop = info.street == 2   # GameInfo.PREFLOP
        agree_num = 0   # the number of player who fixed action
        bet_agree = self.SMALL_BLIND*2 if is_preflop else 0  # bet lower limit
        if is_preflop: pay[info.sb_pos] = self.SMALL_BLIND
        if is_preflop: pay[(info.sb_pos+1)%n] = self.SMALL_BLIND*2

        # keep asking until all players fix their action
        while agree_num < n and len(deactive)<n-1:
            pos = order[i]
            p = players[pos]
            # if player is deactive or allin then skip him
            if p.pid in deactive or p.pid in allin:
                agree_num += 1
                i=(i+1)%n
                continue

            info.set_legal_action(\
                    self.get_legal_action(p, pot, bet_agree, pay[pos]))
            action = p.action(info)
            action = self.correct_action(p, action, pot, bet_agree, pay[pos])
            act, chip = action.split(':')
            chip = int(chip)
            # check if action is raise (raise or raise-allin)
            if bet_agree < chip:
                agree_num = 0
                bet_agree = chip + pay[pos]

            # remove dropped player
            if act == 'FOLD':
                deactive.append(p.pid)
            elif act == 'ALLIN':
                allin.append(p.pid)

            # pay phase
            if act != 'FOLD':
                p.stack -= chip
                pot.add(chip)
                pay[pos] += chip

            i=(i+1)%n
            agree_num += 1

    def correct_action(self, player, action, pot, bet_agree, pay):
        """ check if player's action is legal and correct it if needed.

            Returns:
                action: checked action. if passed action is illegal
                    then it is changed into FOLD:0
        """
        try:
            act, chip = action.split(':')
            chip = int(chip)
            if act == 'RAISE':
                min_raise = max_raise = pot.get_min_raise()
                if chip < min_raise or max_raise < chip:
                    raise ValueError, "> ILLEGAL RAISE => {0}".format(action)
                elif player.getStack() < chip:
                    action = 'ALLIN:{0}'.format(player.getStack())
            elif act == 'CALL':
                if player.getStack() < chip:
                    action = 'ALLIN:{0}'.format(player.getStack())
                elif chip != bet_agree - pay:
                    raise ValueError, "> ILLEGAL CALL => {0}".format(action)
                if chip == 0:
                    action = 'CHECK:0'
            elif act == 'CHECK':
                if bet_agree-pay != 0 or chip != 0:
                    raise ValueError, "> ILLEGAL CHECK => {0}".format(action)
            elif act == 'ALLIN':
                if player.getStack() != chip:
                    raise ValueError, "> ALLIN AMOUNT IS INVALID => {0}".format(action)
            elif act == 'FOLD':
                action = 'FOLD:0'   # convert FOLD:10 into FOLD:0
            else:
                raise ValueError, "> UNKNOWN ACTION => {0}".format(action)
        except ValueError, mes:  # too many values to unpack
            print mes
            action = 'FOLD:0'
        return action

    def get_legal_action(self, player, pot, bet_agree, pay):
        """ provides legal action for player

            Args:
                player: to get legal action
                info: the situation data
                bet_agree: minimum chip to participate in
                pay: the number of chip player have payed in this street
            Returns:
                acts: array of legal action (often 3 action)
        """
        acts = ['FOLD:0']   # FOLD is always legal
        call = '{0}:{1}'.format('CALL' if bet_agree else 'CHECK',bet_agree - pay)
        acts.append(call)
        min_raise = max_raise = pot.get_min_raise()
        _raise = '{0}:{1}:{2}'.format('RAISE',min_raise, max_raise)
        acts.append(_raise)
        return acts


    def check_winner(self, players, deactive, board):
        """ evaluates player's hands and return winner
            
            Returns:
                winner: the array of player who wins the game (multiple player may win)
                result : the array of tuple of hands information (hand(bit flg), hand(str), player)
        """
        winner, result = [], []
        best = -100
        for player in players:
            bit, s = None, None
            if player.pid in deactive:
                bit = -1
                s = player.getName()+" : FOLD"
            else:
                bit = self.E.evalHand(player.getCards(), board.getCards())
                if bit > best: winner = [player]; best = bit
                elif bit == best: winner.append(player)
                s = player.getName()+' : '+self.E.HANDRANK_MAP[self.E.maskHand(bit)]
            result.append((bit,s,player))
        return winner, result

    def money_to_winner(self, pot, players, winner, allin, retire):
        """
        Give pot chip to winner and check if dropped player exists.
        If player's stack is 0, after stack update, then append
        his player id to passed retire array.

        TODO: Not dealing with the case when allin player wins
        """
        n = len(winner)
        win_chip = 1.0*pot.get_chip()/n
        for player in winner:
            player.addStack(win_chip)
        for player in players:
            if player.stack == 0:
                retire.append(player.pid)

    def display_result(self, count, winner, result):
        print '\n*** ROUND '+str(count)+' RESULT ***\n'
        for res in result:
            win = ' ** WINNER **' if res[2] in winner else ''
            print res[1] + '  ('+str(res[2].getStack())+')'+win
        print '\n***********************\n'
