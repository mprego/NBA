# -*- coding: utf-8 -*-
'''
This code contains methods for pulling data from NBA.com
It depends on the NBA_PY package
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

# Creates schedule of games from the NBA website, given a date range (inclusive)
# Returns a DF where each row contains the game, teams, and score
def create_schedule(start_dt, end_dt):
    
    master_game_list=pd.DataFrame()  #will eventually contain a row for each game
    
    for date in pd.date_range(start_dt, end_dt).tolist(): #iterates through given date range
        sb=Scoreboard(month=date.month, day=date.day, year=date.year)
        #time.sleep(1)  #waits for 1 second
        ls=pd.DataFrame(sb.line_score())
        
         # game_list holds all games from the selected date
        game_list=pd.DataFrame(index=range(0,len(ls.index)/2), columns=['Game_ID', 'Date', 'Home Team', 'Home ID', 'Away Team', 'Away ID', 'Home Team Score', 'Away Team Score', 'Home EFG', 'Home TOV', 'Home ORB', 'Home FTFGA', 'Away EFG', 'Away TOV', 'Away ORB', 'Away FTFGA', 'Home Team Win'])
        
        for i in range(0,len(ls.index)/2):      #iterates through each unique game (skips every other entry)
            home_index=2*i      
            away_index=2*i+1
            game=ls.ix[2*i:(2*i+1),:]       #holds the 2 rows corresponding to a single game
            game_list.ix[i,'Game_ID']=ls.ix[home_index,'GAME_ID']
            game_list.ix[i,'Date']=date
            game_list.ix[i,'Home Team']=ls.ix[home_index, 'TEAM_ABBREVIATION']
            game_list.ix[i,'Home ID']=ls.ix[home_index, 'TEAM_ID']
            game_list.ix[i,'Away Team']=ls.ix[away_index, 'TEAM_ABBREVIATION']
            game_list.ix[i,'Away ID']=ls.ix[away_index, 'TEAM_ID']
            game_list.ix[i,'Home Team Score']=sum(ls.ix[home_index,7:21])  #sums up all of the quarters/OTs
            game_list.ix[i,'Away Team Score']=sum(ls.ix[away_index,7:21])
            if game_list.ix[i,'Home Team Score']>game_list.ix[i,'Away Team Score']:
                game_list.ix[i, "Home Team Win"]=1
            else:
                game_list.ix[i, "Home Team Win"]=0
        master_game_list=master_game_list.append(game_list, ignore_index=True)      #appends each game
    return master_game_list
    
    
# Code to test the methods made above
if __name__ == '__main__':
    print create_schedule(dt.datetime(2014,1,1), dt.datetime(2014,1,2))
    
    #signsla code is done
    import os
    os.system("Code is done")
