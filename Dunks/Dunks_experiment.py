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


#==============================================================================
# Adds dunk score data to schedule of games
# Input: pandas df of schedule of games 
# Output: adds dunk scores for each team 
#==============================================================================
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
        if row%5==0:
            print row
        row=row+1
        time.sleep(1)
    return new_data


#==============================================================================
# Creates full schedule by breaking schedule into manageable chunks to add dunk score
# Input: schedule without dunk score
# Output: schedule dunk score
#==============================================================================
def create_dunk_data(schedule):
#    create_schedule(dt.datetime(2014,10,28), dt.datetime(2014,11,30)).to_csv('sched1.csv', index=False)
#    sched1=add_dunk_score(pd.read_csv('sched1.csv'))
#    sched1.to_csv('sched1.csv', index=False)
    
#    create_schedule(dt.datetime(2014,12,1), dt.datetime(2014,12,31)).to_csv('sched2.csv', index=False)
#    sched2=add_dunk_score(pd.read_csv('sched2.csv'))
#    sched2.to_csv('sched2.csv', index=False)
#    
#    create_schedule(dt.datetime(2015,1,1), dt.datetime(2015,1,31)).to_csv('sched3.csv', index=False)
#    sched3=add_dunk_score(pd.read_csv('sched3.csv'))
#    sched3.to_csv('sched3.csv', index=False)
#    
#    create_schedule(dt.datetime(2015,2,1), dt.datetime(2015,2,28)).to_csv('sched4.csv', index=False)
#    sched4=add_dunk_score(pd.read_csv('sched4.csv'))
#    sched4.to_csv('sched4.csv', index=False)
#    
#    create_schedule(dt.datetime(2015,3,1), dt.datetime(2015,3,31)).to_csv('sched5.csv', index=False)
#    sched5=add_dunk_score(pd.read_csv('sched5.csv'))
#    sched5.to_csv('sched5.csv', index=False)
#    
#    create_schedule(dt.datetime(2015,4,1), dt.datetime(2015,4,15)).to_csv('sched6.csv', index=False)
#    sched6=add_dunk_score(pd.read_csv('sched6.csv'))
#    sched6.to_csv('sched6.csv', index=False)
    
    return pd.concat([pd.read_csv('sched1.csv'),pd.read_csv('sched2.csv'), pd.read_csv('sched3.csv'), pd.read_csv('sched4.csv'), pd.read_csv('sched5.csv'), pd.read_csv('sched6.csv')])


#==============================================================================
# Creates scatter plot of dunk score and points with linear regression line overlayed
# Input: Pandas df of schedule with dunk data
# Output: html graph of games and dunk score
#==============================================================================
def plot_scatter(dunk_data, h_x_var, a_x_var, h_y_var, a_y_var, x_title, y_title, title):
    from bokeh.plotting import figure, output_file, show, ColumnDataSource
    from bokeh.models import HoverTool
    # output to static HTML file
    output_file("dunks_graph.html")
    
    x1=dunk_data[h_x_var]
    x1=x1.append(dunk_data[a_x_var])
    x1m=x1.reshape(len(x1),1)
    y1=dunk_data[h_y_var]
    y1=y1.append(dunk_data[a_y_var])    
    y1m=y1.reshape(len(y1), 1)
    Teams=dunk_data['Home Team']
    Teams=Teams.append(dunk_data['Away Team'])   

    # Orange is Home team, Blue is Away Team
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
    
    p = figure(tools=[hover], title=title)
    p.xaxis.axis_label=x_title
    p.yaxis.axis_label=y_title
    p.circle(x1,y1,size=20, color=colors, alpha=0.5, source=source)
    p.line(x1, pred_y, color='red', line_width=5)
    
    # Show the results
    show(p)
    

#==============================================================================
# Creates plot of dunk outcome vs game outcome
# Input: Pandas df of dunk data and game outcomes
# Output: Bar chart of winning percentage by dunk score winner
#==============================================================================
def bar_plot(data):
    from bokeh.charts import Bar, output_file, show
    cat=['Dunk Score Loss', 'Dunk Score Win']
    output_file("dunk_bars.html")
    p=Bar(data, 'Dunk Outcome', values='Winning Pct', agg='mean', title='Dunk Outcome vs Game Outcome')
    show(p)
    
#==============================================================================
# Normalizes scores by removing points by dunks
# Input: Schedule of games with real score and dunk tally
# Output: Schedule of games with adjusted scores and adjusted winners
#==============================================================================
def normalize_dunks(schedule):
    schedule['Home Team Score adj']=schedule['Home Team Score']-2*schedule['h_dunk_made']
    schedule['Away Team Score adj']=schedule['Away Team Score']-2*schedule['a_dunk_made']   
    for i,row in schedule.iterrows():
        if schedule.ix[i,'Home Team Score adj']>schedule.ix[i, 'Away Team Score adj']:
            schedule.ix[i,'Home Team Win adj']=1
        elif schedule.ix[i,'Home Team Score adj']<schedule.ix[i,'Away Team Score adj']:
            schedule.ix[i,'Home Team Win adj']=0
        else:
            schedule.ix[i,'Home Team Win adj']=-1
    return schedule


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
    
    # Creates scatter plot of dunk scores vs game scores
    #plot_scatter(dunk_data, 'h_dunk_score', 'a_dunk_score', 'Home Team Score', 'Away Team Score', 'Dunk Score', 'Game Score', 'Points vs Dunk Score' )
    
    # Prints pearson correlation coefficient
#    import numpy as np
#    x1=dunk_data['h_dunk_score']
#    x1=x1.append(dunk_data['a_dunk_score'])
#    y1=dunk_data['Home Team Score']
#    y1=y1.append(dunk_data['Away Team Score']) 
#    print np.corrcoef(x1,y1)
    
    # Creates scatter plot of dunk outcomes vs game outcomes
#    win_pct_loss=np.mean(dunk_data[dunk_data['h_dunk_win']==0]['Home Team Win'])
#    dunk_outcome_data={'Dunk Outcome':['Dunk Loss', 'Dunk Win'], 'Winning Pct':[win_pct_loss, 1-win_pct_loss]}
#    bar_plot(dunk_outcome_data)
    
    # Normalizes data for dunks made
#    dunk_adj=normalize_dunks(dunk_data)
#    n_total=len(dunk_data)
#    n_match=len(dunk_data[dunk_data['Home Team Win']==dunk_data['Home Team Win adj']])
#    n_undet=len(dunk_data[dunk_data['Home Team Win adj']==-1])
#    n_wrong1=len(dunk_data[dunk_data['Home Team Win adj']==0][dunk_data['Home Team Win']==1])
#    n_wrong2=len(dunk_data[dunk_data['Home Team Win adj']==1][dunk_data['Home Team Win']==0])
#    print 'Total Correct Rate: %.2f%%' %(n_match*100.0/n_total)
#    print 'Selective Correct Rate: %.2f%%' %(n_match*100.0/(n_total-n_undet))
#    
#    # maybe then analyze correlation between dunk score and point differential
#    plot_scatter(dunk_adj, 'h_dunk_score', 'a_dunk_score', 'Home Team Score adj', 'Away Team Score adj', 'Dunk Score', 'Game Score without Dunks', 'Non-Dunk Points vs Dunk Score')
    
    # Prints pearson correlation coefficient
    import numpy as np
    x1=dunk_adj['h_dunk_score']
    x1=x1.append(dunk_adj['a_dunk_score'])
    y1=dunk_adj['Home Team Score adj']
    y1=y1.append(dunk_adj['Away Team Score adj']) 
    print np.corrcoef(x1,y1)