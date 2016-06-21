# -*- coding: utf-8 -*-
"""
This code creates regression models to predict the scores of the games
"""

import numpy as np
import pandas as pd
from sklearn import linear_model, grid_search, ensemble
from sklearn.cross_validation import KFold


class Reg_Model(object):
    """
    Produces a regression model object
    """

    def __init__(self):
        self.best_model = None
        self.tx = None
        self.ty = None
        self.model_type = None
        self.mse = None

#Sets training dataset for the model to be built on
    def set_training(self, x, y):
        self.tx = x
        self.ty = y
        self.cap_and_floor()

#Caps and floors x and y to +/- 2 sd from mean
    def cap_and_floor(self):
        for col in self.tx.columns:
            avg = np.mean(self.tx[col])
            std_dev = np.std(self.tx[col])
            floor = avg - 2*std_dev
            cap = avg + 2*std_dev
            #self.tx[col] = [cap if x>cap else x for x in self.tx[col]]
            #self.tx[col] = [floor if x<floor else x for x in self.tx[col]]
            self.tx.loc[:,col] = [cap if x>cap else x for x in self.tx[col]]
            self.tx.loc[:,col] = [floor if x<floor else x for x in self.tx[col]]
        avg = np.mean(self.ty)
        std_dev = np.std(self.ty)
        floor = avg - 2 * std_dev
        cap = avg + 2 * std_dev
        self.ty = [cap if y>cap else y for y in self.ty]
        self.ty = [floor if y<floor else y for y in self.ty]

    def get_x(self):
        return self.tx

    def get_y(self):
        return self.ty

    def get_mse(self):
        return self.mse
        
    def get_model_type(self):
        return self.model_type
# 
    def ridge_reg(self, x, y):
        rr = linear_model.Ridge()
        parameters = {'alpha': [.1, 1, 10]}
        if len(y) < 10:
            kf = None
        else:
            kf = KFold(n=len(y), n_folds=10, shuffle=True)
        clf = grid_search.GridSearchCV(rr, parameters, scoring = 'mean_squared_error', cv=kf)
        clf.fit(x, y)
        return clf

    def gbm_reg(self, x, y):
        gbm = ensemble.GradientBoostingRegressor()
        parameters = {'learning_rate': [.01, .1, .2, .5], 'max_depth': [1, 3, 5, 10]}
        if len(y) < 10:
            kf = None
        else:
            kf = KFold(n=len(y), n_folds=10, shuffle=True)
        clf = grid_search.GridSearchCV(gbm, parameters, scoring = 'mean_squared_error', cv=kf)
        clf.fit(x, y)
        return clf

    def calc_model(self):
        ridge = self.ridge_reg(self.tx, self.ty)
        gbm = self.gbm_reg(self.tx, self.ty)

        if ridge.best_score_ > gbm.best_score_:
            self.best_model = ridge
            self.model_type = 'ridge'
        else:
            self.best_model = gbm
            self.model_type = 'gbm'
        self.mse = -1* self.best_model.best_score_

    def get_pred(self, test_x):
        if self.best_model == None:
            return None
        else:
            return self.best_model.predict(test_x)






            # if __name__ == '__main__':
            #
            #        # Read in the data
            #    data=pd.read_csv('data.csv')
            #
            #    #first, let's make y equal to the home team's points
            #    y=np.ravel(data['Home Score'])
            #    x_5=data[['Def Dunk Score_a_5', 'Def Dunk Score_h_5', 'Def EFG_a_5',
            #              'Def EFG_h_5', 'Def FTFGA_a_5', 'Def FTFGA_h_5', 'Def ORB_a_5',
            #              'Def ORB_h_5', 'Def TOV_a_5', 'Def TOV_h_5', 'Dunk Score_a_5',
            #              'Dunk Score_h_5', 'EFG_a_5', 'EFG_h_5', 'FTFGA_a_5', 'FTFGA_h_5',
            #              'ORB_a_5', 'ORB_h_5', 'TOV_a_5', 'TOV_h_5', 'Win Pct_a_5',
            #              'Win Pct_h_5', 'BTB_a_5', 'BTB_h_5']]
            #    ridge=ridge_reg(x_5, y)
            #    gbm = gbm_reg(x_5, y)
            #
            #    # pick best model
            #    if ridge.best_score_ > gbm.best_score_:
            #        best_model=ridge
            #    else:
            #        best_model = gbm
            #
            #
            #
            #    # to do list
            #    make function comparing best scores to select the best model to use
            #    also look into using the other variables
