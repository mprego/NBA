import pandas as pd
import numpy as np
from nba_py import player
import os.path


class Player(object):
    '''
    Produces a player object that has various attributes for that player
    '''

    def __init__(self, pid=-1, f_name='', l_name='', season=''):
        self.season = season
        if pid == -1:
            self.f_name = f_name
            self.l_name = l_name
            self.p_id = player.get_player(f_name, l_name).values[0]
            self.desc = self.get_desc()
        else:
            self.p_id = pid
            self.desc = self.get_desc()
            self.f_name = self.desc.ix[0, 'FIRST_NAME']
            self.l_name = self.desc.ix[0, 'LAST_NAME']
        self.game_logs = self.get_game_logs()
        self.model_list = {}

    def set_model(self, target, model):
        self.model_list[target] = model

    def get_desc(self):
        if os.path.isfile('player_desc.csv'):
            saved_player_desc = pd.read_csv('player_desc.csv')
            if len(saved_player_desc[saved_player_desc['P_ID']==self.p_id])>0:
                desc = saved_player_desc[saved_player_desc['P_ID']==self.p_id][['FIRST_NAME', 'LAST_NAME', 'BIRTHDATE', 'HEIGHT', 'WEIGHT', 'SEASON_EXP', 'POSITION', 'ROSTERSTATUS', 'TEAM_ID', 'TEAM_NAME']]
            else:
                desc = player.PlayerSummary(self.p_id).info()[
                    ['FIRST_NAME', 'LAST_NAME', 'BIRTHDATE', 'HEIGHT', 'WEIGHT', 'SEASON_EXP', 'POSITION',
                     'ROSTERSTATUS', 'TEAM_ID', 'TEAM_NAME']]
                desc['P_ID'] = self.p_id
                desc.WEIGHT = desc.WEIGHT.astype(np.int64)
                saved_player_desc = saved_player_desc.append(desc)
        else:
            desc = player.PlayerSummary(self.p_id).info()[['FIRST_NAME', 'LAST_NAME', 'BIRTHDATE', 'HEIGHT', 'WEIGHT', 'SEASON_EXP', 'POSITION', 'ROSTERSTATUS', 'TEAM_ID', 'TEAM_NAME']]
            desc['P_ID'] = self.p_id
            desc.WEIGHT = desc.WEIGHT.astype(np.int64)
            saved_player_desc = desc
        saved_player_desc.to_csv('player_desc.csv', index=False)
        return desc.reset_index(drop=True)

    def get_game_logs(self):
        if os.path.isfile('player_glogs.csv'):
            saved_glogs = pd.read_csv('player_glogs.csv')
            if len(saved_glogs[saved_glogs['Player_ID']==self.p_id])>0:
                game_logs = saved_glogs[saved_glogs['Player_ID']==self.p_id]
            else:
                game_logs = player.PlayerGameLogs(player_id=self.p_id).info()
                saved_glogs = saved_glogs.append(game_logs)
        else:
            game_logs = player.PlayerGameLogs(player_id=self.p_id).info()
            saved_glogs = game_logs
        saved_glogs.to_csv('player_glogs.csv', index=False)
        return game_logs

    def get_stats(self, game_logs, date_col, id_col, target_col, col_list, n):
        stats=pd.DataFrame()
        self.game_logs[date_col] = pd.to_datetime(self.game_logs[date_col])
        for index, g in self.game_logs.sort_values(date_col).iterrows():
            curr_dt = pd.to_datetime(g[date_col])
            past_games = self.game_logs[self.game_logs[date_col]<curr_dt]
            if len(past_games) > n:
                past_games = past_games.sort_values(date_col, ascending=False).head(n)
            stats.set_value(index, id_col, g[id_col])
            stats.set_value(index, target_col, g[target_col])
            stats.set_value(index, 'n_games', len(past_games))
            for col in col_list:
                avg_val = np.mean(past_games[col])
                stats.set_value(index, (col + '_avg_' + str(n)), avg_val)
        return stats
