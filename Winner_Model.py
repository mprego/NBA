# -*- coding: utf-8 -*-
"""
This code creates a SVM and Random Forest model for predicting the outcome of the game
"""

import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import KFold
from sklearn import grid_search
from Four_Factors import *

def svm_model(x,y):
    # SVM modeling
    parameters={'kernel':('linear', 'rbf', 'poly'), 'C':[0.1,.5, 1, 5,10], 'degree':[1,2,3,4]}
    svr=SVC()
    svm=grid_search.GridSearchCV(svr, parameters, cv=kf)
    svm=grid_search.GridSearchCV(svr, parameters)
    svm.fit(x,y)
    print svm.best_score_
    print svm.best_params_
    # ~65%

def ran_forest_model(x,y):
    # Random Forest Modeling
    parameters={'n_estimators':[5,10,20,30,40,50], 'criterion':['gini', 'entropy']}
    rfm=RandomForestClassifier()
    rfm_g=grid_search.GridSearchCV(rfm, parameters, cv=kf)
    rfm_g.fit(x,y)
    print rfm_g.best_score_
    print rfm_g.best_params_
    # ~65%


if __name__ == '__main__':
    # Read in the data
    data=pd.read_csv('data.csv')
    y=np.ravel(data[[23]])
    x=data
    # Drops columns that aren't useful or contain the game outcome
    x.drop(x.columns[[18,23,50,77]], axis=1, inplace=True)
    
    x5=x[x.columns[0:24]]
    x15=x[x.columns[26:50]]
    xn=x[x.columns[52:76]] 
    
    # Drop duplicate columns (BTB indicators)
    x.drop(x.columns[[0,1,24,25,26,27,50,51,76,77]], axis=1, inplace=True)
    
    #Four_Factors.create_scatter(x,y,data)
    
    #Cross Validation Iterator
    kf=KFold(n=len(y), n_folds=10, shuffle=True)
    
    # Test of 5 games
    #svm_model(x5,y) #.64
    #ran_forest_model(x5,y) #.63

    # Test of 15 games
    #svm_model(x15,y) #.66
    #ran_forest_model(x15,y) #.65

    # Test of n games
    #svm_model(xn,y) #.64
    #ran_forest_model(xn,y) #.63

    # Test of all variables
    svm_model(x,y)
    ran_forest_model(x,y)




