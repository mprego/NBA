import pandas as pd
from unittest import TestCase
from Regression.ELO import ELO

class Test_ELO(TestCase):
    def test_get_dates(self):
        schedule = pd.DataFrame(dict(Date={0: '1/1/2000', 1: '1/2/2000', 2: '1/2/2000', 3: '1/3/2000'},
                                     Home={0: 'SA', 1: 'SA', 2: 'HOU', 3: 'DAL'},
                                     Away={0: 'HOU', 1: 'CLE', 2: 'CLE', 3: 'SA'},
                                     h_score={0: 10, 1: 19, 2: 6, 3: 21},
                                     a_score={0: 9, 1: 20, 2: 10, 3: 18}))
        elo = ELO(schedule, 'Date', 'Home', 'Away', 'h_score', 'a_score')
        num_dates = len(elo.elo['SA'])

        exp_num_dates = 3

        self.assertEqual(num_dates, exp_num_dates)

    def test_get_teams(self):
        schedule = pd.DataFrame(dict(Date={0: '1/1/2000', 1: '1/2/2000', 2: '1/2/2000', 3: '1/3/2000'},
                                     Home={0: 'SA', 1: 'SA', 2: 'HOU', 3: 'DAL'},
                                     Away={0: 'HOU', 1: 'CLE', 2: 'CLE', 3: 'SA'},
                                     h_score={0: 10, 1: 19, 2: 6, 3: 21},
                                     a_score={0: 9, 1: 20, 2: 10, 3: 18}))

        elo = ELO(schedule, 'Date', 'Home', 'Away', 'h_score', 'a_score')
        num_teams = len(elo.elo.columns)

        exp_num_teams = 4

        self.assertEqual(num_teams, exp_num_teams)

    def test_first_date(self):
        schedule = pd.DataFrame(dict(Date={0: '1/1/2000', 1: '1/2/2000', 2: '1/2/2000', 3: '1/3/2000'},
                                     Home={0: 'SA', 1: 'SA', 2: 'HOU', 3: 'DAL'},
                                     Away={0: 'HOU', 1: 'CLE', 2: 'CLE', 3: 'SA'},
                                     h_score={0: 10, 1: 19, 2: 6, 3: 21},
                                     a_score={0: 9, 1: 20, 2: 10, 3: 18}))

        elo = ELO(schedule, 'Date', 'Home', 'Away', 'h_score', 'a_score')
        first_date = elo.elo.index[0]

        exp_first_date = '1/1/2000'

        self.assertEqual(first_date, exp_first_date)

    def test_last_date(self):
        schedule = pd.DataFrame(dict(Date={0: '1/1/2000', 1: '1/2/2000', 2: '1/2/2000', 3: '1/3/2000'},
                                     Home={0: 'SA', 1: 'SA', 2: 'HOU', 3: 'DAL'},
                                     Away={0: 'HOU', 1: 'CLE', 2: 'CLE', 3: 'SA'},
                                     h_score={0: 10, 1: 19, 2: 6, 3: 21},
                                     a_score={0: 9, 1: 20, 2: 10, 3: 18}))

        elo = ELO(schedule, 'Date', 'Home', 'Away', 'h_score', 'a_score')
        last_date = elo.elo.index[2]

        exp_last_date = '1/3/2000'

        self.assertEqual(last_date, exp_last_date)

    def test_initial_elo(self):
        schedule = pd.DataFrame(dict(Date={0: '1/1/2000', 1: '1/2/2000', 2: '1/2/2000', 3: '1/3/2000'},
                                     Home={0: 'SA', 1: 'SA', 2: 'HOU', 3: 'DAL'},
                                     Away={0: 'HOU', 1: 'CLE', 2: 'CLE', 3: 'SA'},
                                     h_score={0: 10, 1: 19, 2: 6, 3: 21},
                                     a_score={0: 9, 1: 20, 2: 10, 3: 18}))

        elo = ELO(schedule, 'Date', 'Home', 'Away', 'h_score', 'a_score')
        elo_score = elo.create_elo(1500, 10, 0, 'test').ix['1/1/2000', 'CLE']

        exp_elo_score = 1500

        self.assertEqual(elo_score, exp_elo_score)

    def test_final_elo(self):
        schedule = pd.DataFrame(dict(Date={0: '1/1/2000', 1: '1/2/2000', 2: '1/2/2000', 3: '1/3/2000'},
                                     Home={0: 'SA', 1: 'SA', 2: 'HOU', 3: 'DAL'},
                                     Away={0: 'HOU', 1: 'CLE', 2: 'CLE', 3: 'SA'},
                                     h_score={0: 10, 1: 19, 2: 6, 3: 21},
                                     a_score={0: 9, 1: 20, 2: 10, 3: 18}))

        elo = ELO(schedule, 'Date', 'Home', 'Away', 'h_score', 'a_score')
        elo_score = elo.create_elo(1500, 100, 0, 'test').ix['1/3/2000', 'SA']

        exp_elo_score = 1470

        self.assertEqual(elo_score, exp_elo_score)
        
    def test_k_value(self):
        schedule = pd.DataFrame(dict(Date={0: '1/1/2000', 1: '1/2/2000', 2: '1/2/2000', 3: '1/3/2000'},
                                     Home={0: 'SA', 1: 'SA', 2: 'HOU', 3: 'DAL'},
                                     Away={0: 'HOU', 1: 'CLE', 2: 'CLE', 3: 'SA'},
                                     h_score={0: 10, 1: 19, 2: 6, 3: 21},
                                     a_score={0: 9, 1: 20, 2: 10, 3: 18}))

        elo = ELO(schedule, 'Date', 'Home', 'Away', 'h_score', 'a_score')
        elo_score = elo.create_elo(1500, 0, 0, 'test').ix['1/3/2000', 'SA']

        exp_elo_score = 1500

        self.assertEqual(elo_score, exp_elo_score)

    def test_hca(self):
        schedule = pd.DataFrame(dict(Date={0: '1/1/2000', 1: '1/2/2000', 2: '1/2/2000', 3: '1/3/2000'},
                                     Home={0: 'SA', 1: 'SA', 2: 'HOU', 3: 'DAL'},
                                     Away={0: 'HOU', 1: 'CLE', 2: 'CLE', 3: 'SA'},
                                     h_score={0: 10, 1: 19, 2: 6, 3: 21},
                                     a_score={0: 9, 1: 20, 2: 10, 3: 18}))

        elo = ELO(schedule, 'Date', 'Home', 'Away', 'h_score', 'a_score')
        elo_score = elo.create_elo(1500, 1000, 10, 'test').ix['1/3/2000', 'SA']

        exp_elo_score = 1460

        self.assertEqual(elo_score, exp_elo_score)
        
    def test_538(self):
        schedule = pd.DataFrame(dict(Date={0: '1/1/2000', 1: '1/2/2000', 2: '1/2/2000', 3: '1/3/2000'},
                                     Home={0: 'SA', 1: 'SA', 2: 'HOU', 3: 'DAL'},
                                     Away={0: 'HOU', 1: 'CLE', 2: 'CLE', 3: 'SA'},
                                     h_score={0: 10, 1: 19, 2: 6, 3: 21},
                                     a_score={0: 9, 1: 20, 2: 10, 3: 18}))

        elo = ELO(schedule, 'Date', 'Home', 'Away', 'h_score', 'a_score')
        elo_score = elo.create_elo(1500, 1000, 10, '538').ix['1/3/2000', 'SA']

        exp_elo_score = 1460

        self.assertEqual(elo_score, exp_elo_score)