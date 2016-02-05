# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 20:53:03 2016

@author: Matt
"""

from nba_py import team
import datetime as dt
import pandas as pd
import time
from NBA_API import *

#data=team.TeamShootingSplits(team_id='1610612738', season='2015-16',date_from=dt.datetime(2015,11,27), date_to=dt.datetime(2015,11,27))
#shot_type=data.shot_type_summary() #shows shot type for entire team
#shot_type2=data.shot_type_detail() #lists shot type by playeres

#So i can use the shot_type_summary() to get the team's dunk data for each game based on the schedule
#Then I need to filter out the dunks and the missed dunks

# Adds dunk score data to schedule of games
def add_dunk_score(schedule):
    new_data=schedule.reset_index(drop=True)
    row=0
    for i in range(0,len(new_data)):#new_data.iterrows():
        t0=time.clock()
        home_data=team.TeamShootingSplits(team_id=schedule.ix[row, 'Home ID'], season='2014-15',date_from=schedule.ix[row, 'Date'], date_to=schedule.ix[row, 'Date'])
        print time.clock()-t0
        home_shooting=home_data.shot_type_summary()
        h_dunk=home_shooting[home_shooting['GROUP_VALUE'].isin(['Dunk Shot', 'Putback Dunk Shot', 'Putback Slam Dunk Shot', 'Slam Dunk Shot'])]
        h_score=2*h_dunk['FGM'].sum()-h_dunk['FGA'].sum()
        away_data=team.TeamShootingSplits(team_id=schedule.ix[row, 'Away ID'], season='2014-15',date_from=schedule.ix[row, 'Date'], date_to=schedule.ix[row, 'Date'])
        away_shooting=away_data.shot_type_summary()  
        a_dunk=away_shooting[away_shooting['GROUP_VALUE'].isin(['Dunk Shot', 'Putback Dunk Shot', 'Putback Slam Dunk Shot', 'Slam Dunk Shot'])]
        a_score=2*a_dunk['FGM'].sum()-a_dunk['FGA'].sum()
        
        new_data.ix[row,'h_dunk_score']=h_score
        new_data.ix[row,'a_dunk_score']=a_score
        if h_score>a_score:
            new_data.ix[row,'h_dunk_win']=1
        elif h_score==a_score:
            new_data.ix[row,'h_dunk_win']=-1
        else:
            new_data.ix[row,'h_dunk_win']=0
        if row%5==0:
            print row
        row=row+1
    return new_data


# Breaks schedule into manageable chunks to add dunk score
def create_dunk_data(schedule):
    #create_schedule(dt.datetime(2014,10,28), dt.datetime(2014,11,30)).to_csv('sched1.csv', index=False)
    #sched1=add_dunk_score(pd.read_csv('sched1.csv'))
    #sched1.to_csv('sched1.csv', index=False)
    
#    #create_schedule(dt.datetime(2014,12,1), dt.datetime(2014,12,31)).to_csv('sched2.csv', index=False)
#    sched2=add_dunk_score(pd.read_csv('sched2.csv'))
#    sched2.to_csv('sched2.csv', index=False)
    
#    #create_schedule(dt.datetime(2015,1,1), dt.datetime(2015,1,31)).to_csv('sched3.csv', index=False)
#    sched3=add_dunk_score(pd.read_csv('sched3.csv'))
#    sched3.to_csv('sched3.csv', index=False)
#    
#    #create_schedule(dt.datetime(2015,2,1), dt.datetime(2015,2,28)).to_csv('sched4.csv', index=False)
#    sched4=add_dunk_score(pd.read_csv('sched4.csv'))
#    sched4.to_csv('sched4.csv', index=False)
#    
#    #create_schedule(dt.datetime(2015,3,1), dt.datetime(2015,3,31)).to_csv('sched5.csv', index=False)
#    sched5=add_dunk_score(pd.read_csv('sched5.csv'))
#    sched5.to_csv('sched5.csv', index=False)
#    
#    #create_schedule(dt.datetime(2015,4,1), dt.datetime(2015,4,15)).to_csv('sched6.csv', index=False)
#    sched6=add_dunk_score(pd.read_csv('sched6.csv'))
#    sched6.to_csv('sched6.csv', index=False)
#    
    return pd.concat([pd.read_csv('sched1.csv'),pd.read_csv('sched2.csv'), pd.read_csv('sched3.csv'), pd.read_csv('sched4.csv'), pd.read_csv('sched5.csv'), pd.read_csv('sched6.csv')])



if __name__ == '__main__':
    #Adds Dunk data to schedule of games
#    schedule=pd.read_csv('schedule.csv')
#    dunk_data=create_dunk_data(schedule)
#    dunk_data.to_csv('dunk_data.csv', index=False)

    #Analyzes to see connection between dunks and winning
    dunk_data=pd.read_csv('dunk_data.csv')
#    n_total=len(dunk_data)
#    n_match=len(dunk_data[dunk_data['Home Team Win']==dunk_data['h_dunk_win']])
#    n_undet=len(dunk_data[dunk_data['h_dunk_win']==-1])
#    n_wrong1=len(dunk_data[dunk_data['h_dunk_win']==0][dunk_data['Home Team Win']==1])
#    n_wrong2=len(dunk_data[dunk_data['h_dunk_win']==1][dunk_data['Home Team Win']==0])
#    print 'Total Correct Rate: %.2f%%' %(n_match*100.0/n_total)
#    print 'Selective Correct Rate: %.2f%%' %(n_match*100.0/(n_total-n_undet))
#    
    
    from bokeh.plotting import figure, output_file, show, ColumnDataSource
    from bokeh.models import HoverTool
    import numpy as np

    # output to static HTML file
    output_file("line.html")
    
    x1=dunk_data['h_dunk_score']
    x1=x1.append(dunk_data['a_dunk_score'])
    x1m=x1.reshape(len(x1),1)
    y1=dunk_data['Home Team Score']
    y1=y1.append(dunk_data['Away Team Score'])    
    y1m=y1.reshape(len(y1), 1)
    Teams=dunk_data['Home Team']
    Teams=Teams.append(dunk_data['Away Team'])   

    
    colors=['orange']*(len(x1)/2)+ ['blue']*(len(x1)/2)
    
    from sklearn import linear_model
    model=linear_model.LinearRegression()
    model.fit(x1m,y1m)
    pred_ym=model.predict(x1m)
    pred_y=pred_ym.reshape(len(pred_ym),)
    
    source = ColumnDataSource(
        data=dict(
            x=x1,
            y=y1,
            desc=Teams,
        )
    )

    hover = HoverTool(
        tooltips=[
            ("Team", "@desc"),
            ("Dunk Score", "@x"),
            ("Score", "@y"),
        ]
    )
    
    p = figure(tools=[hover], title='Points vs Dunk Score')
    p.xaxis.axis_label='Dunk Score'
    p.yaxis.axis_label='Game Score'
    p.circle(x1,y1,size=20, color=colors, alpha=0.5, source=source)
    p.line(x1, pred_y, color='red', line_width=5)
    
     #show the results
    show(p)
    