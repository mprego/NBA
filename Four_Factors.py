# -*- coding: utf-8 -*-
"""
Analysis on the Four Factors and the outcome of games
"""

#Import packages
import numpy as np
import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models import HoverTool
from bokeh.io import gridplot
from sklearn.cross_validation import KFold
from sklearn import grid_search

def create_scatter(x,y,schedule, var):
    source = ColumnDataSource(data=dict(desc=schedule[[var]],))
    hover = HoverTool(tooltips=[("Game", "@desc"),])
    p=figure(tools=[hover], title='%s vs Win' %var, plot_width=300, plot_height=300)
    p.scatter(x[var], y, source=source)
    p.line([np.mean(schedule[schedule['Home Team Win']==0][var]),
             np.mean(schedule[schedule['Home Team Win']==1][var])],[0,1], line_color='red', line_width=5)
    return p

def explore_vars(x,y, schedule):
    output_file("scatter.html")

    p1=create_scatter(x,y,schedule, 'Home EFG')
    p2=create_scatter(x,y,schedule, 'Home TOV')
    p3=create_scatter(x,y,schedule, 'Home ORB')
    p4=create_scatter(x,y,schedule, 'Home FTFGA')
    
    p=gridplot([[p1,p2],[p3,p4]])
    
    show(p)
    
def logit_model(x,y):
    ym=np.ravel(y)
    kf=KFold(n=len(y), n_folds=10, shuffle=True)
    mlr=linear_model.LogisticRegression()
    mlr.cv=grid_search.GridSearchCV(mlr, {'C':[1]}, cv=kf)
    mlr.cv.fit(x,ym)
    print mlr.cv.best_score_

if __name__ == '__main__':
    # Reads in schedule of 2014-2015 NBA season
    schedule=pd.read_csv('schedule.csv')    
    x=schedule[['Home EFG', 'Home TOV', 'Home ORB', 'Home FTFGA', 'Away EFG', 'Away TOV', 'Away ORB', 'Away FTFGA']]
    y=schedule[['Home Team Win']]

    
    explore_vars(x,y, schedule)   
    
    # Exclude outliers from dataset
    outliers=[21400144, 21400370, 21400555, 21400437, 21401022, 21400512, 21401073, 21400003]
    x=schedule[~schedule.Game_ID.isin(outliers)][['Home EFG', 'Home TOV', 'Home ORB', 'Home FTFGA', 'Away EFG', 'Away TOV', 'Away ORB', 'Away FTFGA']]
    y=schedule[~schedule.Game_ID.isin(outliers)][['Home Team Win']]
    
    logit_model(x,y)
