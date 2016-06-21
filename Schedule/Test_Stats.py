from unittest import TestCase
from Stats import Stats
import pandas as pd

class Test_Stats(TestCase):
    def test_get_last_n_games(self):
        games = pd.DataFrame({'Date': {1: '1/1/2015', 2: '1/2/2015', 3: '1/3/2015'},
                              'H_Team_ID': {1: 1, 2: 1, 3: 2},
                               'A_Team_ID': {1: 3, 2: 2, 3: 1},
                              'Score': {1:1, 2:2, 3:3}})
        stats = Stats(games, 'test', 'Date', 'H_Team_ID', 'A_Team_ID', None,[])
        last1 = len(stats.get_last_n_games(1, 1, '1/3/2015'))
        exp_last1 = 1
        self.assertEqual(last1, exp_last1)
        last2 = len(stats.get_last_n_games(4, 1, '1/3/2015'))
        exp_last2 = 2
        self.assertEqual(last2, exp_last2)

    def test_get_avg(self):
        games = pd.DataFrame({'Date': {1: '1/1/2015', 2: '1/2/2015', 3: '1/3/2015'},
                              'H_Team_ID': {1: 1, 2: 1, 3: 2},
                              'A_Team_ID': {1: 3, 2: 2, 3: 1},
                              'A_Score': {1: 1, 2: 2, 3: 3},
                              'H_Score': {1: 2, 2: 2, 3: 2}})
        stats = Stats(games, 'test', 'Date', 'H_Team_ID', 'A_Team_ID', None,[])
        av = stats.get_avg(games, 'Score', 1, 0)
        exp_av = 7.0/3
        self.assertEqual(av, exp_av)
        avo = stats.get_avg(games, 'Score', 1, 1)
        exp_avo = 5.0 / 3
        self.assertEqual(avo, exp_avo)

    def test_lastn_stats(self):
        games = pd.DataFrame({'Date': {1: '1/1/2015', 2: '1/2/2015', 3: '1/3/2015'},
                              'H_Team_ID': {1: 1, 2: 1, 3: 2},
                              'A_Team_ID': {1: 3, 2: 2, 3: 1},
                              'A_Score': {1: 1, 2: 2, 3: 3},
                              'H_Score': {1: 2, 2: 2, 3: 2},
                              'Outcome': {1: 1, 2:0, 3:1}})
        stats = Stats(games, 'test', 'Date', 'H_Team_ID', 'A_Team_ID', 'Outcome',['test'])
        l1 = stats.get_lastn_stats(1)
        size = len(l1)
        exp_size = 3
        self.assertEqual(size, exp_size)
        cols = set(l1.columns.values)
        exp_cols = set(['Outcome', 'H_Score_1', 'A_Score_1', 'H_O_Score_1', 'A_O_Score_1'])
        self.assertEqual(cols, exp_cols)
        t1 = l1.ix[3,'H_Score_1']
        exp_t1 = 2
        self.assertEqual(t1, exp_t1)
        l2 = stats.get_lastn_stats(2)
        t2 = l2.ix[3, 'A_Score_2']
        exp_t2 = 2
        self.assertEqual(t2, exp_t2)
        t21 = l2.ix[1, 'A_Score_2']
        exp_t21 = -1
        self.assertEqual(t21, exp_t21)
        t2o = l2.ix[3, 'H_O_Score_2']
        exp_t2o = 2
        self.assertEqual(t2o, exp_t2o)