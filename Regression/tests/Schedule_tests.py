# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 21:36:01 2016

@author: Matt
"""

import pandas as pd
from unittest import TestCase

from Regression.Schedule import Schedule

class TestSchedule(TestCase):
    def test_date(self):
        sched = Schedule('2014-2015', '10/28/14', '10/29/14')
        beg_dt = sched.get_beg_dt()
        
        exp_beg_dt = pd.to_datetime('10/28/14')
        
        self.assertEqual(beg_dt, exp_beg_dt)
        
    def test_games_helper(self):
        sched = Schedule('2014-2015', '10/28/14', '10/29/14')
        game1 = sched.get_games_helper(pd.to_datetime('10/28/14'), pd.to_datetime('10/29/14')).ix[0, 'Home Team']
        
        exp_game1 = 'ORL'
        
        self.assertEqual(game1, exp_game1)
        
    def test_games(self):
        sched = Schedule('2014-2015', '10/28/14', '10/29/14')
        game1 = sched.get_games().ix[0, 'Home Team']
        
        exp_game1 = 'ORL'
        
        self.assertEqual(game1, exp_game1)
        
    def test_last_n_games(self):
        sched = Schedule('2014-2015', '10/28/14', '11/5/14')
        last_n = len(sched.get_last_n_games(1610612753, '11/2/14', 2))
        
        exp_last_n = 2
        
        self.assertEqual(last_n, exp_last_n)
        
    def test_no_last_n_games(self):
        sched = Schedule('2014-2015', '10/29/14', '10/30/14')
        last_games = sched.get_last_n_games(1610612753, '10/30/14', 4)
        if last_games is not None:
            last_n = len(last_games)
        else:
            last_n = 0
        
        exp_last_n = 0
        
        self.assertEqual(last_n, exp_last_n)
        
    def test_last_n_stats(self):
        sched = Schedule('2014-2015', '10/28/14', '11/5/14')
        last_n_stats = sched.get_stats(1610612753, '11/2/14', 22, 2).ix[0,1]
        
        exp_last_n_stats = 1
        
        self.assertEqual(last_n_stats, exp_last_n_stats)

    def test_season_f(self):
        sched = Schedule('2014-2015', '10/28/14', '11/5/14')
        season = sched.create_season_f()
        exp_season = '2014 - 15'
        self.assertEqual(season, exp_season)
        
