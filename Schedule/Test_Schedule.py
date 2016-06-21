from unittest import TestCase
from Schedule import Schedule
import pandas as pd

class Test_Schedule(TestCase):
    def test_get_season_name(self):
        sched = Schedule('1/1/2001', '2/1/2001')
        name = sched.get_season_name()
        exp_name = '2000-01'
        self.assertEqual(name, exp_name)

        sched = Schedule('11/1/2001', '12/1/2001')
        name = sched.get_season_name()
        exp_name = '2001-02'
        self.assertEqual(name, exp_name)

    def test_games(self):
        sched = Schedule('1/1/2015')
        games = sched.get_games()
        size = len(games)
        exp_size = 1230
        self.assertEqual(size, exp_size)
        cols = len(games.columns)
        exp_cols = 40 + 4
        self.assertEqual(cols, exp_cols)

    def test_team_list(self):
        sched = Schedule('1/1/2015')
        _list = sched.get_team_list()
        _len = len(_list)
        exp_len = 30
        self.assertEqual(_len, exp_len)

    # def test_four_factors_helper(self):
    #     df = pd.DataFrame({'FGM': {1: 5, 2:5},
    #                        '3PM': {1: 2, 2:2},
    #                        'FGA': {1:10, 2:10},
    #                        'ORB': {1:1, 2:1},
    #                        'DRB': {1:10, 2:10},
    #                        'O_ORB': {1:1, 2:1},
    #                        'O_DRB': {1: 10, 2: 10},
    #                        'TO':{1:5, 2:5},
    #                        'FTM':{1:5, 2:5},
    #                        'FTA':{1:10, 2:10}
    #                        })
    #     sched = Schedule('1/1/2015')
    #     ff = sched.add_four_factors_helper(df, '_', 'FGM', '3PM', 'FGA', 'ORB', 'O_DRB', 'TO', 'FTM', 'FTA')
    #     efg = ff.ix[1,'_EFG']
    #     exp_efg = .6
    #     self.assertEqual(efg, exp_efg)
    #     tov = ff.ix[1, '_TOV']
    #     exp_tov = 5/(10+10*.44-1+5)
    #     self.assertEqual(tov, exp_tov)
    #     orb = ff.ix[1, '_ORB']
    #     exp_orb = 1.0/11
    #     self.assertEqual(orb, exp_orb)
    #     ftfga = ff.ix[1, '_FTFGA']
    #     exp_ftfga = .5
    #     self.assertEqual(ftfga, exp_ftfga)
    #
    # def test_four_factors(self):
    #     sched = Schedule('1/1/2015')
    #     ff = sched.add_four_factors()
    #     cols = len(ff.columns)
    #     exp_cols = 44 + 8
    #     self.assertEqual(cols, exp_cols)
    #
    # def test_dunk_data(self):
    #     sched = Schedule('1/1/2015', '1/2/2015')
    #     dunk = sched.add_dunk_data()
    #     cols = len(dunk.columns)
    #     exp_cols = 44 + 6
    #     self.assertEqual(cols, exp_cols)
