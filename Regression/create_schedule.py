# -*- coding: utf-8 -*-
'''
This code creates statistics for each game to be used in the model
'''

#Imports Packages
from nba_py import *
from nba_py import team
from nba_py import game
from nba_py.constants import *
#from Dunks_experiment import *
import pandas as pd
import datetime as dt
import numpy as np
import time

# Selects subset of schedule for last n games for a specified team
# Requires Team_ID, current date (finds games before), number of games, and full schedule
def lastNGames(team_id, end_dt, n, schedule):
    home_last=schedule.ix[schedule['Home ID']==team_id]     #filters for only games where specified team is involved
    away_last=schedule.ix[schedule['Away ID']==team_id]
    last=pd.concat([home_last, away_last])
    last['Date']=pd.to_datetime(last['Date'])       #converts the date columns to datetime
    last=last[last['Date']<end_dt]      #filters by games that occur before date specified
    last=last.sort_values('Date', ascending=False)
    last=last.reset_index(drop=True)
    length=min(n,len(last))
    lastn=pd.DataFrame(index=range(0,length), columns=['Date', 'Game ID', 'Team ID', 'Home', 'Score', 'Opp Score', 'Win', 'EFG', 'Opp EFG', 'TOV', 'Opp TOV', 'ORB', 'Opp ORB', 'FTFGA', 'Opp FTFGA', 'Dunk Score', 'Opp Dunk Score', 'Dunk Win'])    
    for i in range(0,length):
        lastn.ix[i,'Date']=last.ix[i, 'Date']
        lastn.ix[i,'Team ID']=team_id
        lastn.ix[i,'Game ID']=last.ix[i,'Game_ID']
        if last.ix[i, 'Home ID']==team_id:
            lastn.ix[i,'Home']=1
            lastn.ix[i,'Score']=last.ix[i,'Home Team Score']
            lastn.ix[i,'Opp Score']=last.ix[i,'Away Team Score']
            lastn.ix[i,'EFG']=last.ix[i,'Home EFG']
            lastn.ix[i,'Opp EFG']=last.ix[i,'Away EFG']
            lastn.ix[i,'TOV']=last.ix[i,'Home TOV']
            lastn.ix[i,'Opp TOV']=last.ix[i,'Away TOV']
            lastn.ix[i,'ORB']=last.ix[i,'Home ORB']
            lastn.ix[i,'Opp ORB']=last.ix[i,'Away ORB']
            lastn.ix[i,'FTFGA']=last.ix[i,'Home FTFGA']
            lastn.ix[i,'Opp FTFGA']=last.ix[i,'Away FTFGA']
            lastn.ix[i,'Dunk Score']=last.ix[i,'h_dunk_score']
            lastn.ix[i,'Opp Dunk Score']=last.ix[i,'a_dunk_score']
        else:
            lastn.ix[i,'Home']=0
            lastn.ix[i,'Score']=last.ix[i,'Away Team Score']
            lastn.ix[i,'Opp Score']=last.ix[i,'Home Team Score']
            lastn.ix[i,'EFG']=last.ix[i,'Away EFG']
            lastn.ix[i,'Opp EFG']=last.ix[i,'Home EFG']
            lastn.ix[i,'TOV']=last.ix[i,'Away TOV']
            lastn.ix[i,'Opp TOV']=last.ix[i,'Home TOV']
            lastn.ix[i,'ORB']=last.ix[i,'Away ORB']
            lastn.ix[i,'Opp ORB']=last.ix[i,'Home ORB']
            lastn.ix[i,'FTFGA']=last.ix[i,'Away FTFGA']
            lastn.ix[i,'Opp FTFGA']=last.ix[i,'Home FTFGA']
            lastn.ix[i,'Dunk Score']=last.ix[i,'a_dunk_score']
            lastn.ix[i,'Opp Dunk Score']=last.ix[i,'h_dunk_score']
        if lastn.ix[i,'Score']>lastn.ix[i,'Opp Score']:
            lastn.ix[i,'Win']=1
        else:
            lastn.ix[i,'Win']=0
        if lastn.ix[i,'Dunk Score']>lastn.ix[i,'Opp Dunk Score']:
            lastn.ix[i,'Dunk Win']=1
        else:
            lastn.ix[i,'Dunk Win']=0
    return lastn


# Returns stats for the last n games for a given team and game
# Requires team, current date, game on current date, number of games to go back, and full schedule
def lastNStats(team_id, end_dt, game_id, n, schedule):
    lastngames=lastNGames(team_id, end_dt, n, schedule)
    lastnstats=pd.DataFrame(index=range(0,1), columns=['Game_ID', 'BTB', 'n games', 'Win Pct', 'EFG', 'Def EFG', 'TOV', 'Def TOV', 'ORB', 'Def ORB', 'FTFGA', 'Def FTFGA', 'Dunk Score', 'Def Dunk Score'])
    lastnstats.ix[0,'Game_ID']=game_id
    lastnstats.ix[0,'n games']=len(lastngames.ix[:,0])
    if lastnstats.ix[0,'n games'] ==0:       #if there are no previous games
        lastnstats.ix[0, 'BTB']=0
        for c in range(0,11):
            lastnstats.ix[0,c+3]=0
    else:
        if (end_dt-lastngames.ix[0,'Date']).days==1:
            lastnstats.ix[0,'BTB']=1
        else:
            lastnstats.ix[0,'BTB']=0
        for c in range(0,11):
            lastnstats.ix[0,c+3]=np.mean(lastngames.ix[:,c+6])
    return lastnstats
    
    
# Creates the 2014-2015 NBA schedule with the 4 factors added in
def create_2014_schedule():
    create_schedule(dt.datetime(2014,10,28), dt.datetime(2014,11,30)).to_csv('sched1.csv', index=False)
    sched1=add_factors(pd.read_csv('sched1.csv'))
    sched1.to_csv('sched1.csv', index=False)
    
    create_schedule(dt.datetime(2014,12,1), dt.datetime(2014,12,31)).to_csv('sched2.csv', index=False)
    sched2=add_factors(pd.read_csv('sched2.csv'))
    sched2.to_csv('sched2.csv', index=False)
    
    create_schedule(dt.datetime(2015,1,1), dt.datetime(2015,1,31)).to_csv('sched3.csv', index=False)
    sched3=add_factors(pd.read_csv('sched3.csv'))
    sched3.to_csv('sched3.csv', index=False)
    
    create_schedule(dt.datetime(2015,2,1), dt.datetime(2015,2,28)).to_csv('sched4.csv', index=False)
    sched4=add_factors(pd.read_csv('sched4.csv'))
    sched4.to_csv('sched4.csv', index=False)
    
    create_schedule(dt.datetime(2015,3,1), dt.datetime(2015,3,31)).to_csv('sched5.csv', index=False)
    sched5=add_factors(pd.read_csv('sched5.csv'))
    sched5.to_csv('sched5.csv', index=False)
    
    create_schedule(dt.datetime(2015,4,1), dt.datetime(2015,4,15)).to_csv('sched6.csv', index=False)
    sched6=add_factors(pd.read_csv('sched6.csv'))
    sched6.to_csv('sched6.csv', index=False)
    
    schedule=pd.concat([sched1, sched2, sched3, sched4, sched5, sched6])
    
    # Adds in Dunk Data for each team 
    schedule_dd=create_dunk_data(schedule)
    
    return scheudle_dd
        

# Creates DF of games with all input variables necessary for stats model
# Requires start and end date (inclusive), number of n games back, and DF of entire schedule
def create_train_data(st_dt, end_dt, n, schedule):
    schedule['Date']=pd.to_datetime(schedule['Date'])
    score_set=schedule[schedule['Date']>=st_dt]
    score_set=score_set[score_set['Date']<=end_dt]
    score_set=score_set.reset_index(drop=True)
    data=pd.DataFrame()
    for row in range(len(score_set)):
        data_h=lastNStats(score_set.ix[row, 'Home ID'], score_set.ix[row,'Date'], score_set.ix[row, 'Game_ID'], n,schedule)
        data_a=lastNStats(score_set.ix[row, 'Away ID'], score_set.ix[row,'Date'], score_set.ix[row, 'Game_ID'], n,schedule)
        data=data.append(pd.merge(data_h, data_a, how='inner', on='Game_ID', suffixes=('_h', '_a')))
        data=data.reset_index(drop=True)
        data.ix[row, 'Win']=score_set.ix[row, 'Home Team Win']
        data.ix[row, 'Home Score']=score_set.ix[row, 'Home Team Score']
        data.ix[row, 'Away Score']=score_set.ix[row, 'Away Team Score']
    return data  
    


# Code to test the methods made above
if __name__ == '__main__':
    
    #code to make dataset of 5 and 15 last games in datset
    season_start=dt.datetime(2014,10,28)  #start date for 2014-2015 season
    season_end=dt.datetime(2015,4,15)     #end date for 2014-2015 season
    
    #schedule=create_2014_schedule()
#    schedule=pd.read_csv('schedule.csv')

#    data5=create_train_data(dt.datetime(2014,11,15), dt.datetime(2015,4,10), 5, schedule)
#    data15=create_train_data(dt.datetime(2014,11,15), dt.datetime(2015,4,10), 15, schedule)
#    data_all=create_train_data(dt.datetime(2014,11,15), dt.datetime(2015,4,10), 82, schedule)
#    data=pd.merge(data5, data15, how='inner', on='Game_ID', suffixes=('_5', '_15'))
#    data=pd.merge(data, data_all, how='inner', on='Game_ID', suffixes=('', '_all'))
#    data.to_csv('data.csv', index=False)
   