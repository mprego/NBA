import pandas as pd
import numpy as np

class Stats(object):
    '''
    Produces stats given a schedule
    '''
    def __init__(self, games, agg_method, date_col, h_col, a_col, outcome_col, seg_vars = []):
        self.games = games
        self.agg_method = agg_method
        self.date_col = date_col
        self.h_col = h_col
        self.a_col = a_col
        self.outcome_col = outcome_col
        self.seg_vars = seg_vars

# Inputs: number of past games, team id, date of current game
# Output: list of most recent n games
    def get_last_n_games(self, n, team_id, curr_dt):
        #Filter to get past games
        games = self.games[self.games[self.date_col]<curr_dt]
        #Filters to get past home and away games
        a_games = games[games[self.a_col]==team_id]
        h_games = games[games[self.h_col] == team_id]
        all_games = a_games.append(h_games)
        all_games['temp_days'] = [(pd.to_datetime(curr_dt) - pd.to_datetime(x)).days for x in all_games[self.date_col]]
        all_games = all_games[all_games['temp_days']<=30]
        all_games = all_games.drop('temp_days', axis=1)
        all_games = all_games.sort_values(by=self.date_col, ascending=False)
        n_games = all_games.head(n)
        return n_games

    def get_avg(self, games, col, team_id, opp):
        h_games = games[games[self.h_col] == team_id]
        a_games = games[games[self.a_col] == team_id]
        if opp == 0:
            a_col = 'A_' + col
            h_col = 'H_' + col
        else:
            a_col = 'H_' + col
            h_col = 'A_' + col
        h_sum = np.sum(h_games[h_col])
        a_sum = np.sum(a_games[a_col])
        if len(games) == 0:
            return -1
        avg = (h_sum + a_sum)*1.0 / (len(games))
        return avg

    def back_to_back(self, games, curr_dt):
        if len(games)==0:
            return 0
        latest_game = games.sort_values(by=self.date_col, ascending=False).head(1).reset_index(drop=True)
        latest_date = latest_game.ix[0,self.date_col]
        if (pd.to_datetime(curr_dt) - pd.to_datetime(latest_date)).days == 1:
            return 1
        return 0

    def get_lastn_stats(self, n):
        stats = pd.DataFrame()
        for index, game in self.games.iterrows():
            stats.set_value(index, self.outcome_col, game[self.outcome_col])
            a_team = game[self.a_col]
            a_games = self.get_last_n_games(n, a_team, game[self.date_col])
            h_team = game[self.h_col]
            h_games = self.get_last_n_games(n, h_team, game[self.date_col])
            poss_cols = self.games.columns.values
            poss_cols = self.search_for_cols('H_', poss_cols)
            for col in poss_cols:
                base_col = col[2:]
                stats.set_value(index, ('H_' + base_col + '_' + str(n)), self.get_avg(h_games, base_col, h_team, 0))
                stats.set_value(index, ('H_O_' + base_col + '_' + str(n)), self.get_avg(h_games, base_col, h_team, 1))
                stats.set_value(index, ('A_' + base_col + '_' + str(n)), self.get_avg(a_games, base_col, a_team, 0))
                stats.set_value(index, ('A_O_' + base_col + '_' + str(n)), self.get_avg(a_games, base_col, a_team, 1))
            stats.set_value(index, 'H_BTB', self.back_to_back(h_games, game[self.date_col]))
            stats.set_value(index, 'A_BTB', self.back_to_back(a_games, game[self.date_col]))
            stats.set_value(index, 'H_'+str(n)+'_games', len(h_games))
            stats.set_value(index, 'A_'+str(n)+'_games', len(a_games))
            for col in self.seg_vars:
                stats.set_value(index, col, game[col])
        return stats

    def search_for_cols(self, pfx, cols):
        new_cols = []
        pfx_len = len(pfx)
        for col in cols:
            if col[0:pfx_len] == pfx:
                #if col != self.outcome_col:
                if col != self.h_col:
                    if col != self.a_col:
                        new_cols.append(col)
        return new_cols

    def get_correl(self, stats):
        cor = pd.DataFrame()
        for col in stats.columns.values:
            if col != self.outcome_col:
                cor.set_value(col, 'Correlation', np.corrcoef(x=stats[col], y=stats[self.outcome_col])[0,1])
        return cor