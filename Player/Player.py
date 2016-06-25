import pandas as pd
import numpy as np
from nba_py import player

class Player(object):
    '''
    Produces a player object that has various attributes for that player
    '''

    def __init__(self, pid=-1, f_name='', l_name='', season=''):
        self.season = season
        if pid == -1:
            self.f_name = f_name
            self.l_name = l_name
            self.p_id = player.get_player(f_name, l_name)
            self.desc = self.get_desc()
        else:
            self.p_id = pid
            self.desc = self.get_desc()
            self.f_name = self.desc.ix[0, 'FIRST_NAME']
            self.l_name = self.desc.ix[0, 'LAST_NAME']
        self.game_logs = self.get_game_logs()

    def get_desc(self):
        desc = player.PlayerSummary(self.p_id).info()[['FIRST_NAME', 'LAST_NAME', 'BIRTHDATE', 'HEIGHT', 'WEIGHT', 'SEASON_EXP', 'POSITION', 'ROSTERSTATUS', 'TEAM_ID', 'TEAM_NAME']]
        desc.WEIGHT = desc.WEIGHT.astype(np.int64)
        return desc

    def get_game_logs(self):
        game_logs = player.PlayerGameLogs(player_id=self.p_id).info()
        return game_logs