from unittest import TestCase
from Player import Player
from Players import Players
import pandas as pd


class Test_Player(TestCase):
    def test_desc(self):
        player = Player(f_name='Lebron', l_name='James', season='2015-16')
        weight = player.desc.iloc[0]['WEIGHT']
        exp_weight = 250
        self.assertEqual(weight, exp_weight)

    def test_game_logs(self):
        player = Player(f_name='Lebron', l_name='James', season='2015-16')
        fg_pct = player.game_logs.iloc[0]['FG_PCT']
        exp_fg_pct = 0.813
        self.assertEqual(fg_pct, exp_fg_pct)

    def test_player_list(self):
        p_list = Players('2015-16')
        size = len(p_list.player_list)
        exp_size = 476
        self.assertEqual(size, exp_size)