from unittest import TestCase
from Player import Player
from Players import Players
import pandas as pd


class Test_Player(TestCase):
    # def test_desc(self):
    #     player = Player(f_name='Lebron', l_name='James', season='2015-16')
    #     weight = player.desc.iloc[0]['WEIGHT']
    #     exp_weight = 250
    #     self.assertEqual(weight, exp_weight)
    #
    # def test_game_logs(self):
    #     player = Player(f_name='Lebron', l_name='James', season='2015-16')
    #     fg_pct = player.game_logs.iloc[0]['FG_PCT']
    #     exp_fg_pct = 0.813
    #     self.assertEqual(fg_pct, exp_fg_pct)
    #
    # def test_player_byid(self):
    #     player = Player(pid=203112)
    #     weight = player.desc.iloc[0]['WEIGHT']
    #     exp_weight = 240
    #     self.assertEqual(weight, exp_weight)
    #
    # def test_player_list(self):
    #     p_list = Players('2015-16', 10)
    #     size = len(p_list.player_list)
    #     exp_size = 11
    #     self.assertEqual(size, exp_size)
    #
    # def test_players(self):
    #     p_list = Players('2015-16',10)
    #     name = p_list.players[203112].desc.ix[0,'LAST_NAME']
    #     exp_name = 'Acy'
    #     self.assertEqual(name, exp_name)

    def test_stats(self):
        player = Player(pid=203112)
        data = player.get_stats('GAME_DATE', 'Game_ID', 'PTS', ['PTS', 'MIN', 'FGM', 'FGA', 'FG_PCT'], 2)
        avg = data[data['Game_ID']==21500103].reset_index(drop=True).ix[0,'PTS_avg']
        exp_avg = 1.5
        self.assertEqual(avg, exp_avg)
        avg_min = data[data['Game_ID']==21500103].reset_index(drop=True).ix[0,'MIN_avg']
        exp_avg_min = 19.0/2
        self.assertEqual(avg_min, exp_avg_min)

