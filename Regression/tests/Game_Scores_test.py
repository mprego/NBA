# -*- coding: utf-8 -*-
"""
Created on Sun May 29 20:30:41 2016

@author: Matt
"""

import pandas as pd
from unittest import TestCase
from Regression.Game_Scores import Game_Scores


class Test_Scores(TestCase):
    def test_x_vars(self):
        schedule = pd.DataFrame(
            {'x1': [1, 2, 3, 4], 'x2': [4, 3, 2, 1], 'Win': [1, 1, 1, 1], 'home': [4, 5, 6, 7], 'away': [2, 3, 4, 5]})
        scores = Game_Scores(schedule, ['x1', 'x2'], 'Win', 'home', 'away')
        x_value = scores.get_x_vars().ix[0, 0]

        expected_x_value = 1

        self.assertEqual(x_value, expected_x_value)

    def test_y_vars(self):
        schedule = pd.DataFrame(
            {'x1': [1, 2, 3, 4], 'x2': [4, 3, 2, 1], 'Win': [1, 1, 1, 1], 'home': [4, 5, 6, 7], 'away': [2, 3, 4, 5]})
        scores = Game_Scores(schedule, ['x1', 'x2'], 'Win', 'home', 'away')
        y_value = scores.get_home_scores()[0]

        expected_y_value = 4

        self.assertEqual(y_value, expected_y_value)

    def test_pred(self):
        schedule = pd.DataFrame(
            {'x1': [1, 2, 3, 4], 'x2': [4, 3, 2, 1], 'Win': [1, 1, 1, 1], 'home': [4, 5, 6, 7], 'away': [2, 3, 4, 5]})
        scores = Game_Scores(schedule, ['x1', 'x2'], 'Win', 'home', 'away')
        pred = int(scores.get_pred_home(schedule[['x1', 'x2']])[0])

        exp_pred = 4

        self.assertEqual(pred, exp_pred)

    def test_accuracy(self):
        schedule = pd.DataFrame(
            {'x1': [1, 2, 3, 4], 'x2': [4, 3, 2, 1], 'Win': [1, 1, 1, 1], 'home': [4, 5, 6, 7], 'away': [2, 3, 4, 5]})
        scores = Game_Scores(schedule, ['x1', 'x2'], 'Win', 'home', 'away')
        acc = scores.get_accuracy()

        exp_acc = 1

        self.assertEqual(acc, exp_acc)

    def test_win_score(self):
        schedule = pd.DataFrame(
            {'x1': [1, 2, 3, 4], 'x2': [4, 3, 2, 1], 'Win': [1, 1, 1, 1], 'home': [4, 5, 6, 7], 'away': [2, 3, 4, 5]})
        scores = Game_Scores(schedule, ['x1', 'x2'], 'Win', 'home', 'away')
        win_score = scores.get_win_scores(schedule[['x1', 'x2']])[0]

        exp_win_score = .52

        self.assertEqual(win_score, exp_win_score)

    def test_rank_order(self):
        schedule = pd.DataFrame(
            {'x1': [1, 2, 3], 'x2': [4, 3, 2], 'Win': [0, 1, 1], 'home': [4, 5, 6], 'away': [5, 4, 3]})
        scores = Game_Scores(schedule, ['x1', 'x2'], 'Win', 'home', 'away')
        rank_order = scores.get_rank_order_acc().ix[.51, 'Cum Win']

        #exp_rank_order = pd.DataFrame({0.51: .5, 0.53: 1, 0.49: 0.0})
        exp_rank_order = .5

        self.assertEqual(rank_order, exp_rank_order)

    def test_rank_order_count(self):
        schedule = pd.DataFrame(
            {'x1': [1, 2, 3], 'x2': [4, 3, 2], 'Win': [0, 1, 1], 'home': [4, 5, 6], 'away': [5, 4, 3]})
        scores = Game_Scores(schedule, ['x1', 'x2'], 'Win', 'home', 'away')
        count = scores.get_rank_order_acc().ix[.51,'Cum Count']

        #exp_count = pd.DataFrame({0.51: 1, 0.53: 1, 0.49: 1})
        exp_count = 2.0/3

        self.assertEqual(count, exp_count)

import pandas as pd
import Game_Scores
schedule = pd.DataFrame(
    {'x1': [1, 2, 3], 'x2': [4, 3, 2], 'Win': [0, 1, 1], 'home': [4, 5, 6], 'away': [5, 4, 3]})
scores = Game_Scores(schedule, ['x1', 'x2'], 'Win', 'home', 'away')
scores.create_rank_order_graph()

