import pandas as pd
import numpy as np

class ELO(object):
    '''
    Creates ELO scores for each team
    '''
    def __init__(self, schedule, date_col, h_team_col, a_team_col, h_score, a_score):
        self.games = pd.DataFrame()
        self.games['Date'] = schedule[date_col]
        self.games['h_team'] = schedule[h_team_col]
        self.games['a_team'] = schedule[a_team_col]
        self.games['h_score'] = schedule[h_score]
        self.games['a_score'] = schedule[a_score]
        dates = sorted(list(set(schedule[date_col])))
        teams = set(schedule[h_team_col].append(schedule[a_team_col]))
        self.elo = pd.DataFrame(index = dates, columns = teams)

    def create_elo(self, base_score, k, hca, method):
        for col in self.elo.columns:
            self.elo.ix[0,col] = base_score
        #self.elo.ix[0:] = [base_score]*(len(self.elo.columns))
        index = 0
        for date in self.elo.index.values:  
            if index>0:
                self.elo.ix[date, :] = self.elo.ix[index-1, :]
            game_subset = self.games[self.games['Date']==date]
            for i, game in game_subset.iterrows():
                h_team = game['h_team']
                a_team = game['a_team']
                h_elo = self.elo.ix[date, h_team]
                a_elo = self.elo.ix[date, a_team]

                elo_diff = h_elo - a_elo - hca
                score_diff = game['h_score'] - game['a_score']
    
                if method == '538':
                    if (elo_diff * score_diff) >0:
                        elo_swap = ((abs(score_diff)+3)**0.8) / (7.5+0.006 * abs(elo_diff))
                    else:
                        elo_swap = ((abs(score_diff)+3)**0.8) / (7.5+0.006 * abs(elo_diff) * -1)
                elif method =='test':
                    elo_swap = 10*score_diff - elo_diff
                elo_swap = min(elo_swap, k)
                elo_swap = max(elo_swap, -k)
                    
                self.elo.set_value(date, h_team, h_elo + elo_swap)
                self.elo.set_value(date, a_team, a_elo - elo_swap)
            index +=1
#            
#        index = 0    
#        for i, date in self.elo.iterrows():
#            for col in range(len(self.elo.columns)):
#                if np.isnan(self.elo.ix[i, col]):
#                    self.elo.ix[i, col] = self.elo.ix[(index-1), col]
#            index += 1
#    
        return self.elo
