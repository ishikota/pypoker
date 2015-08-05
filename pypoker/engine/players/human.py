from base_player import BasePlayer

class Human(BasePlayer):
    """
        This player class receives action from stdin.
        So human player can play poker games by using this class in the game.
    """
    def __init__(self, pid, player_name, start_stack):
        super(Human, self).__init__(pid, player_name, start_stack)

    def action(self, info):
        if info.street == 0:
            return  # human player do nothing when NEW GAME begins
        info.display()
        print self.getName()+' > input your action,'
        print '    Legal Action : '+str(self.getLegalAction(info))
        print '    Your card : '+str(self.cardsToString())
        print '    1: fold, 2: call or check, 3: raise'
        while True:
            try:
                a = int(raw_input())
                if a == 0: break
            except:  # input is not integer
                print '> Error: Choose input from [1(fold), 2(call), 3(raise) ]'
                continue
            if a !=1 and a!=2 and a!=3:
                print '> Error: Choose input from [1(fold), 2(call), 3(raise) ]'
            else:
                if a == 3: # if raise
                    print '> how much do you raise? (??<=pay<=??)'
                    while True:
                        try:
                            pay = int(raw_input())
                        except:
                            print '> Error: Raise amount must be integer'
                            continue
                        return 'RAISE:'+str(pay)
            return 'FOLD:0' if a == 1 else 'CALL:0'
