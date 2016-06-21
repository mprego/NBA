# -*- coding: utf-8 -*-
'''
This code creates statistics for each game to be used in the model
'''

#Imports Packages
from nba_py import *
from nba_py import team
from nba_py import game
from nba_py.constants import *
import pandas as pd
import datetime as dt
import numpy as np
import time
import os.path

class Schedule(object):
    '''
    Produces an object that returns a schedule of games and data
    '''
    
    def __init__(self, season, beg_dt, end_dt):
        self.season=season
        if self.season == '14-15':
            self.season_f = '2014-15'
        elif self.season == '15-16':
            self.season_f = '2015-16'
        else:
            self.season_f = '2014-15'
        self.beg_dt = pd.to_datetime(beg_dt)
        self.end_dt = pd.to_datetime(end_dt)
        self.games = None
        self.scoring_set = None
        games_fn = 'games_' + season + '.csv'
        if os.path.isfile(games_fn):
            self.games = pd.read_csv(games_fn)

        self.get_games()

    def create_season_f(self):
        beg_year = self.beg_dt.year
        end_year = beg_year + 1
        self.season_f = str(beg_year) + '-' + str(end_year)[3:]
        return self.season_f

    def get_beg_dt(self):
        return self.beg_dt        

    def set_games(self, games):
        self.games = games

    def get_games(self):
        if self.games is None:
            self.games = pd.DataFrame()
            b_date = self.beg_dt
            e_date = b_date + dt.timedelta(days=29)
            while(True):
                if e_date >= self.end_dt:
                    games = self.get_games_helper(b_date, self.end_dt)
                    self.games = self.games.append(games, ignore_index=True)
                    return self.games
                else:
                    games = self.get_games_helper(b_date, e_date)
                    self.games = self.games.append(games, ignore_index=True)
                    b_date = b_date + dt.timedelta(days=30)
                    e_date = e_date + dt.timedelta(days=30)
                    self.games.to_csv('checkpoint.csv', index = False)
                    time.sleep(30)
        self.transform_games()
        return self.games
        
    def get_games_helper(self, b_date, e_date):
        master_game_list=pd.DataFrame()  #will eventually contain a row for each game

        for date in pd.date_range(b_date, e_date).tolist(): #iterates through given date range
            sb=Scoreboard(month=date.month, day=date.day, year=date.year)
            #time.sleep(1)  #waits for 1 second
            ls=pd.DataFrame(sb.line_score())
             # game_list holds all games from the selected date
            game_list=pd.DataFrame(index=range(0,len(ls.index)/2), columns=['Game_ID', 'Date', 'Home Team', 'Home ID', 'Away Team', 'Away ID', 'H_PTS', 'A_PTS', 'Home EFG', 'Home TOV', 'Home ORB', 'Home FTFGA', 'Away EFG', 'Away TOV', 'Away ORB', 'Away FTFGA', 'H_WL', 'A_WL'])
            
            for i in range(0,len(ls.index)/2):      #iterates through each unique game (skips every other entry)
                home_index=2*i      
                away_index=2*i+1
                game_list.ix[i,'Game_ID']=ls.ix[home_index,'GAME_ID']
                game_list.ix[i,'Date']=date
                game_list.ix[i,'Home Team']=ls.ix[home_index, 'TEAM_ABBREVIATION']
                game_list.ix[i,'Home ID']=ls.ix[home_index, 'TEAM_ID']
                game_list.ix[i,'Away Team']=ls.ix[away_index, 'TEAM_ABBREVIATION']
                game_list.ix[i,'Away ID']=ls.ix[away_index, 'TEAM_ID']
                game_list.ix[i,'H_PTS']=sum(ls.ix[home_index,7:21])  #sums up all of the quarters/OTs
                game_list.ix[i,'A_PTS']=sum(ls.ix[away_index,7:21])
                if game_list.ix[i,'Home Team Score']>game_list.ix[i,'Away Team Score']:
                    game_list.ix[i, "H_WL"]=1
                    game_list.ix[i, "A_WL"] = 0
                else:
                    game_list.ix[i, "H_WL"] = 0
                    game_list.ix[i, "A_WL"] = 1
            master_game_list=master_game_list.append(game_list, ignore_index=True)      #appends each game
        #master_game_list = self.add_four_factors(master_game_list)
        #master_game_list = self.add_dunk_score(master_game_list)
        return master_game_list

    def transform_games(self):
        self.games['Pts_diff'] = [x - y for x, y in zip(self.games['PTS_home'], self.games['PTS_away'])]
        self.games = self.games[['Pts_diff', 'H_PTS', 'A_PTS', 'GAME_DATE', 'Home Team', 'Away Team']]

        
    def add_four_factors(self, sched):
        new_data=sched.reset_index(drop=True)
        row=0
        for i in new_data.iterrows():
            game_ID='00'+str(int(new_data.ix[row,'Game_ID']))
            four_factors=game.BoxscoreFourFactors(game_ID)
            #time.sleep(1)
            factors_data=four_factors.sql_team_four_factors()
            home_ID=int(new_data.ix[row, 'Home ID'])
            if home_ID==factors_data.ix[0,'TEAM_ID']:
                h_index=0
                a_index=1
            else:
                a_index=0
                h_index=1
            new_data.ix[row,'Home EFG']=factors_data.ix[h_index,'EFG_PCT']
            new_data.ix[row,'Home TOV']=factors_data.ix[h_index,'TM_TOV_PCT']
            new_data.ix[row,'Home ORB']=factors_data.ix[h_index,'OREB_PCT']
            new_data.ix[row,'Home FTFGA']=factors_data.ix[h_index,'FTA_RATE']
            new_data.ix[row,'Away EFG']=factors_data.ix[a_index,'EFG_PCT']
            new_data.ix[row,'Away TOV']=factors_data.ix[a_index,'TM_TOV_PCT']
            new_data.ix[row,'Away ORB']=factors_data.ix[a_index,'OREB_PCT']
            new_data.ix[row,'Away FTFGA']=factors_data.ix[a_index,'FTA_RATE']
            row=row+1
        return new_data        
        
    def add_dunk_score(self, schedule):
        new_data=schedule.reset_index(drop=True)
        row=0
        for i in range(0,len(new_data)):#new_data.iterrows():
            home_data=team.TeamShootingSplits(team_id=schedule.ix[row, 'Home ID'], season=self.season_f,date_from=schedule.ix[row, 'Date'], date_to=schedule.ix[row, 'Date'])
            home_shooting=home_data.shot_type_summary()
            h_dunk=home_shooting[home_shooting['GROUP_VALUE'].isin(['Dunk Shot', 'Putback Dunk Shot', 'Putback Slam Dunk Shot', 'Slam Dunk Shot'])]
            h_score=2*h_dunk['FGM'].sum()-h_dunk['FGA'].sum()
            away_data=team.TeamShootingSplits(team_id=schedule.ix[row, 'Away ID'], season=self.season_f,date_from=schedule.ix[row, 'Date'], date_to=schedule.ix[row, 'Date'])
            away_shooting=away_data.shot_type_summary()  
            a_dunk=away_shooting[away_shooting['GROUP_VALUE'].isin(['Dunk Shot', 'Putback Dunk Shot', 'Putback Slam Dunk Shot', 'Slam Dunk Shot'])]
            a_score=2*a_dunk['FGM'].sum()-a_dunk['FGA'].sum()
            
            new_data.ix[row, 'h_dunk_made']=h_dunk['FGM'].sum()
            new_data.ix[row, 'h_dunk_miss']=h_dunk['FGA'].sum()-h_dunk['FGM'].sum()        
            new_data.ix[row, 'a_dunk_made']=a_dunk['FGM'].sum()
            new_data.ix[row, 'a_dunk_miss']=a_dunk['FGA'].sum()-a_dunk['FGM'].sum()
            new_data.ix[row,'h_dunk_score']=h_score
            new_data.ix[row,'a_dunk_score']=a_score
            if h_score>a_score:
                new_data.ix[row,'h_dunk_win']=1
            elif h_score==a_score:
                new_data.ix[row,'h_dunk_win']=-1
            else:
                new_data.ix[row,'h_dunk_win']=0
#            if row%5==0:
#                print row
            row=row+1
            time.sleep(1)
        return new_data

    def get_last_n_games(self, team_id, curr_dt, n):
        if self.games is None:
            self.get_games()
        home = self.games[self.games['Home ID']==team_id]
        away = self.games[self.games['Away ID']==team_id]
        last_n = pd.concat([home, away])        
        last_n['Date'] = pd.to_datetime(last_n['Date'])
        last_n = last_n[last_n['Date']<curr_dt]
        last_n = last_n.sort_values('Date', ascending = False)
        last_n = last_n.reset_index(drop = True)
        num_games = min(n, len(last_n['Game_ID']))
        
        if len(last_n['Game_ID']) < 1:
            return None
        
        ln_games = pd.DataFrame(index=range(0, num_games))
        
        for i in range(0, num_games):
            ln_games.ix[i,'Date']=last_n.ix[i, 'Date']
            ln_games.ix[i,'Team ID']=team_id
            ln_games.ix[i,'Game ID']=last_n.ix[i,'Game_ID']
            if last_n.ix[i, 'Home ID']==team_id:
                ln_games.ix[i,'Home']=1
                ln_games.ix[i,'Score']=last_n.ix[i,'Home Team Score']
                ln_games.ix[i,'Opp Score']=last_n.ix[i,'Away Team Score']
                ln_games.ix[i,'EFG']=last_n.ix[i,'Home EFG']
                ln_games.ix[i,'Opp EFG']=last_n.ix[i,'Away EFG']
                ln_games.ix[i,'TOV']=last_n.ix[i,'Home TOV']
                ln_games.ix[i,'Opp TOV']=last_n.ix[i,'Away TOV']
                ln_games.ix[i,'ORB']=last_n.ix[i,'Home ORB']
                ln_games.ix[i,'Opp ORB']=last_n.ix[i,'Away ORB']
                ln_games.ix[i,'FTFGA']=last_n.ix[i,'Home FTFGA']
                ln_games.ix[i,'Opp FTFGA']=last_n.ix[i,'Away FTFGA']
#                ln_games.ix[i,'Dunk Score']=last_n.ix[i,'h_dunk_score']
#                ln_games.ix[i,'Opp Dunk Score']=last_n.ix[i,'a_dunk_score']
            else:
                ln_games.ix[i,'Home']=0
                ln_games.ix[i,'Score']=last_n.ix[i,'Away Team Score']
                ln_games.ix[i,'Opp Score']=last_n.ix[i,'Home Team Score']
                ln_games.ix[i,'EFG']=last_n.ix[i,'Away EFG']
                ln_games.ix[i,'Opp EFG']=last_n.ix[i,'Home EFG']
                ln_games.ix[i,'TOV']=last_n.ix[i,'Away TOV']
                ln_games.ix[i,'Opp TOV']=last_n.ix[i,'Home TOV']
                ln_games.ix[i,'ORB']=last_n.ix[i,'Away ORB']
                ln_games.ix[i,'Opp ORB']=last_n.ix[i,'Home ORB']
                ln_games.ix[i,'FTFGA']=last_n.ix[i,'Away FTFGA']
                ln_games.ix[i,'Opp FTFGA']=last_n.ix[i,'Home FTFGA']
#                ln_games.ix[i,'Dunk Score']=last_n.ix[i,'a_dunk_score']
#                ln_games.ix[i,'Opp Dunk Score']=last_n.ix[i,'h_dunk_score']
            if ln_games.ix[i,'Score']>ln_games.ix[i,'Opp Score']:
                ln_games.ix[i,'Win']=1
            else:
                ln_games.ix[i,'Win']=0
#            if ln_games.ix[i,'Dunk Score']>ln_games.ix[i,'Opp Dunk Score']:
#                ln_games.ix[i,'Dunk Win']=1
#            else:
#                ln_games.ix[i,'Dunk Win']=0
        return ln_games
        
    def get_stats(self, team_id, curr_dt, game_id, n):
        ln_games = self.get_last_n_games(team_id, curr_dt, n)
        ln_stats = pd.DataFrame(index=range(0,1), columns=['Game_ID', 'BTB', 'n games', 'Win Pct', 'EFG', 'Def EFG', 'TOV', 'Def TOV', 'ORB', 'Def ORB', 'FTFGA', 'Def FTFGA', 'Dunk Score', 'Def Dunk Score'])
        if ln_games is None:
            return ln_stats
        ln_stats.set_value(0, 'Game_ID', game_id)
        ln_stats.set_value(0, 'n games', len(ln_games['Win']))
        if ln_stats.ix[0, 'n games'] == 0:
            ln_stats.set_value(0, 'BTB', 0)
            for c in range(0,11):
                ln_stats.set_value(0, c+3, 0)
        else:
            if(pd.to_datetime(curr_dt) - ln_games.ix[0, 'Date']).days == 1:
                ln_stats.set_value(0, 'BTB', 1)
            else:
                ln_stats.set_value(0, 'BTB', 0)
            for c in range(0,9):
                ln_stats.set_value(0, c+3, np.mean(ln_games.ix[:, c+6]))
        return ln_stats
    
        
    
# Creates DF of games with all input variables necessary for stats model
# Requires start and end date (inclusive), number of n games back, and DF of entire schedule
    def get_scoring_set(self, n):
        if self.games is None:
            self.get_games()
        score_set = self.games.reset_index(drop=True)
        self.scoring_set=pd.DataFrame()
        for row in range(len(score_set)):
            data_h= self.get_stats(score_set.ix[row, 'Home ID'], score_set.ix[row,'Date'], score_set.ix[row, 'Game_ID'], n)
            data_a= self.get_stats(score_set.ix[row, 'Away ID'], score_set.ix[row,'Date'], score_set.ix[row, 'Game_ID'], n)
            self.scoring_set = self.scoring_set.append(pd.merge(data_h, data_a, how='inner', on='Game_ID', suffixes=('_h', '_a')))
            self.scoring_set = self.scoring_set.reset_index(drop=True)
            self.scoring_set.ix[row, 'Win']=score_set.ix[row, 'Home Team Win']
            self.scoring_set.ix[row, 'Home Score']=score_set.ix[row, 'Home Team Score']
            self.scoring_set.ix[row, 'Away Score']=score_set.ix[row, 'Away Team Score']
        return self.scoring_set  
        
    
       