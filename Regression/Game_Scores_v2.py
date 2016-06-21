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

    def __init__(self, schedule, x, target_name):
        self.x = x
        self.target = schedule[target_name]
        self.answers = [1 if x>0 else 0 for x in schedule[target_name]]
        self.pred = None
        self.win_scores = None
        self.rank_order = None
        self.model = Reg_Model()
        self.model.set_training(self.x, self.target)
        self.model.calc_model()


#Returns df of features
    def get_x_vars(self):
        return self.x

#Returns model
    def get_model(self):
        return self.model

#For some test accounts, returns the predictions
    def get_pred(self, test_x):
        self.pred = self.model.get_pred(test_x)
        return self.pred

#Looks at training data and returns overall accuracy
    def get_accuracy(self):
        pred = self.model.get_pred(self.x)
        win_pred = [1 if x > 0 else 0 for x in pred]
        accuracy = sum([1 if x == y else 0 for x, y in zip(win_pred, self.answers)]) * 1.0 / len(self.answers)
        return accuracy

#Returns score linked to probability of winning
    def get_win_scores(self, test_x):
        if self.pred == None:
            self.get_pred(test_x)
        self.win_scores = [round((50 + x) / 100, 2) for x in (self.pred)]
        return self.win_scores

#Returns cumulative accuracy by win_score
    def get_rank_order_acc(self):
        if self.win_scores == None:
            self.get_win_scores(self.x)
        set_ws = sorted(list(set(self.win_scores)))
        self.rank_order = pd.DataFrame(index=set_ws)
        data = pd.DataFrame()
        data['answers'] = self.answers
        data['pred'] = self.pred
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
            self.get_rank_order_acc()
        x = self.rank_order['Cum Count']
        y = self.rank_order['Cum Win']
        plt.scatter(x,y, alpha=.5)
        plt.show()

