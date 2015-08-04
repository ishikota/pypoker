from engine.ui.hand_evaluator import HandEvaluator

class Dealer(object):
    
    # CONSTANTS
    SMALL_BLIND = 5

    def __init__(self):
        self.E = HandEvaluator()

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

            action = p.action(info)
            #action = check_action(p, act, info)
            act, chip = action.split(':')
            chip = int(chip)
            # check if action is raise (raise or raise-allin)
            if bet_agree < chip:
                agree_num = 0
                bet_agree = chip

            # remove dropped player
            if act == 'FOLD':
                deactive.append(p.pid)
            elif act == 'ALLIN':
                allin.append(p.pid)

            # pay phase
            if act != 'FOLD':
                shortage = chip - pay[pos]
                p.stack -= shortage
                pot.chip += shortage
                pay[pos] = chip

            i=(i+1)%n
            agree_num += 1



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

    def money_to_winner(self):
        pass


