from base_player import BasePlayer
from engine.ui.game_info import GameInfo

class MockPlayer(BasePlayer):
    '''
        This player just returns defined action,
        so you can define this AI behavior, by setting sequence of action.
        
    '''
    
    def __init__(self, pid, player_name, start_stack):
        super(MockPlayer, self).__init__(pid, player_name, start_stack)
        self.act_index = 0
        self.actions = []
        self.D = False  # debug flg

    def set_action(self, actions):
        self.actions = actions

    def action(self, info):
        if info and info.street == GameInfo.NEWGAME:
            return
        action = self.actions[self.act_index%len(self.actions)]
        self.act_index += 1
        if self.D: print "{0}:{1}".format(self.NAME, action)
        return action
