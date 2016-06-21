# -*- coding: utf-8 -*-
"""
Created on Sun May 29 20:24:06 2016

@author: Matt
"""

from Reg_Model import Reg_Model
import pandas as pd
import matplotlib.pyplot as plt


class Game_Scores(object):
    """
    Takes a set of games for training and makes model from them
    """

    def __init__(self, schedule, x_var, target_name, home_score_name, away_score_name):
        self.x = schedule[x_var]
        self.home_score = schedule[home_score_name]
        self.away_score = schedule[away_score_name]
        self.answers = schedule[target_name].tolist()
        self.home_pred = None
        self.away_pred = None
        self.win_scores = None
        self.rank_order = None
        self.home_model = Reg_Model()
        self.home_model.set_training(self.x, self.home_score)
        self.home_model.calc_model()
        self.away_model = Reg_Model()
        self.away_model.set_training(self.x, self.away_score)
        self.away_model.calc_model()

#Returns df of features
    def get_x_vars(self):
        return self.x

#Returns home scores
    def get_home_scores(self):
        return self.home_score
        
#Returns home model
    def get_home_model(self):
        return self.home_model

#Returns away scores
    def get_away_scores(self):
        return self.away_score
        
#Returns away model
    def get_away_model(self):
        return self.away_model

#For some test accounts, returns the predictions
    def get_pred_home(self, test_x):
        self.home_pred = self.home_model.get_pred(test_x)
        return self.home_pred

    def get_pred_away(self, test_x):
        self.away_pred = self.away_model.get_pred(test_x)
        return self.away_pred

#Looks at training data and returns overall accuracy
    def get_accuracy(self):
        home_pred = self.home_model.get_pred(self.x)
        away_pred = self.away_model.get_pred(self.x)
        win_pred = [1 if x > 0 else 0 for x in (home_pred - away_pred)]
        accuracy = sum([1 if x == y else 0 for x, y in zip(win_pred, self.answers)]) * 1.0 / len(self.answers)
        return accuracy

#Returns score linked to probability of winning
    def get_win_scores(self, test_x):
        if self.home_pred == None:
            self.get_pred_home(test_x)
        if self.away_pred == None:
            self.get_pred_away(test_x)
        self.win_scores = [round((50 + x) / 100, 2) for x in (self.home_pred - self.away_pred)]
        return self.win_scores

#Returns cumulative accuracy by win_score
    def get_rank_order_acc(self):
        if self.win_scores == None:
            self.get_win_scores(self.x)
        set_ws = sorted(list(set(self.win_scores)))
        self.rank_order = pd.DataFrame(index=set_ws)
        data = pd.DataFrame()
        data['home'] = self.home_pred
        data['away'] = self.away_pred
        data['answers'] = self.answers
        data['pred'] = self.home_pred - self.away_pred
        data['win_scores'] = self.win_scores
        cum_win = 0
        cum_count = 0
        total_win = sum(data['answers'])
        total_count = len(data['answers'])
        for ro in set_ws:
            game_subset = data[data['win_scores'] == ro]
            win_pred = [1 if x > 0 else 0 for x in game_subset['pred']]
            num_correct = sum([1 if x==y else 0 for x,y in zip(win_pred, game_subset['answers'])])
            sum_win = sum(game_subset['answers'])
            cum_win += sum_win
            cum_count += len(game_subset['answers'])
            self.rank_order.set_value(ro, 'Cum Win', 1.0 * cum_win / total_win)
            self.rank_order.set_value(ro, 'Cum Count', 1.0 * cum_count / total_count)
            self.rank_order.set_value(ro, 'Accuracy', 1.0 * num_correct / len(game_subset['answers']))
        return self.rank_order

#Returns graph of cumulative rank_order
    def create_rank_order_graph(self):
        if self.rank_order is None:
            self.rank_order_acc()
        x = self.rank_order['Cum Count']
        y = self.rank_order['Cum Win']
        plt.scatter(x,y, alpha=.5)
        plt.show()

