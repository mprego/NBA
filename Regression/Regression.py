# -*- coding: utf-8 -*-
"""
Created on Mon May 30 08:00:41 2016

@author: Matt
"""

from Game_Scores import Game_Scores
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('data.csv')

# first, let's make y equal to the home team's points
# y=np.ravel(data['Home Score'])
# x=data[['Def Dunk Score_a_5', 'Def Dunk Score_h_5', 'Def EFG_a_5',
#              'Def EFG_h_5', 'Def FTFGA_a_5', 'Def FTFGA_h_5', 'Def ORB_a_5',
#              'Def ORB_h_5', 'Def TOV_a_5', 'Def TOV_h_5', 'Dunk Score_a_5',
#              'Dunk Score_h_5', 'EFG_a_5', 'EFG_h_5', 'FTFGA_a_5', 'FTFGA_h_5',
#              'ORB_a_5', 'ORB_h_5', 'TOV_a_5', 'TOV_h_5', 'Win Pct_a_5',
#              'Win Pct_h_5', 'BTB_a_5', 'BTB_h_5']]

# scores_5 = Game_Scores(data, ['Def Dunk Score_a_5', 'Def Dunk Score_h_5', 'Def EFG_a_5',
#              'Def EFG_h_5', 'Def FTFGA_a_5', 'Def FTFGA_h_5', 'Def ORB_a_5',
#              'Def ORB_h_5', 'Def TOV_a_5', 'Def TOV_h_5', 'Dunk Score_a_5',
#              'Dunk Score_h_5', 'EFG_a_5', 'EFG_h_5', 'FTFGA_a_5', 'FTFGA_h_5',
#              'ORB_a_5', 'ORB_h_5', 'TOV_a_5', 'TOV_h_5', 'Win Pct_a_5',
#              'Win Pct_h_5', 'BTB_a_5', 'BTB_h_5'], 'Home Score', 'Away Score')
# print '5 game accuracy:', scores_5.get_accuracy(data['Win'])
#
# scores_15 = Game_Scores(data, ['Def Dunk Score_a_15', 'Def Dunk Score_h_15', 'Def EFG_a_15',
#              'Def EFG_h_15', 'Def FTFGA_a_15', 'Def FTFGA_h_15', 'Def ORB_a_15',
#              'Def ORB_h_15', 'Def TOV_a_15', 'Def TOV_h_15', 'Dunk Score_a_15',
#              'Dunk Score_h_15', 'EFG_a_15', 'EFG_h_15', 'FTFGA_a_15', 'FTFGA_h_15',
#              'ORB_a_15', 'ORB_h_15', 'TOV_a_15', 'TOV_h_15', 'Win Pct_a_15',
#              'Win Pct_h_15', 'BTB_a_15', 'BTB_h_15'], 'Home Score', 'Away Score')
# print '15 game accuracy:', scores_15.get_accuracy(data['Win'])
#
# scores_all = Game_Scores(data, ['Def Dunk Score_a_5', 'Def Dunk Score_h_5', 'Def EFG_a_5',
#              'Def EFG_h_5', 'Def FTFGA_a_5', 'Def FTFGA_h_5', 'Def ORB_a_5',
#              'Def ORB_h_5', 'Def TOV_a_5', 'Def TOV_h_5', 'Dunk Score_a_5',
#              'Dunk Score_h_5', 'EFG_a_5', 'EFG_h_5', 'FTFGA_a_5', 'FTFGA_h_5',
#              'ORB_a_5', 'ORB_h_5', 'TOV_a_5', 'TOV_h_5', 'Win Pct_a_5',
#              'Win Pct_h_5', 'BTB_a_5', 'BTB_h_5', 'Def Dunk Score_a_15', 'Def Dunk Score_h_15', 'Def EFG_a_15', 
#              'Def EFG_h_15', 'Def FTFGA_a_15', 'Def FTFGA_h_15', 'Def ORB_a_15',
#              'Def ORB_h_15', 'Def TOV_a_15', 'Def TOV_h_15', 'Dunk Score_a_15',
#              'Dunk Score_h_15', 'EFG_a_15', 'EFG_h_15', 'FTFGA_a_15', 'FTFGA_h_15',
#              'ORB_a_15', 'ORB_h_15', 'TOV_a_15', 'TOV_h_15', 'Win Pct_a_15',
#              'Win Pct_h_15', 'BTB_a_15', 'BTB_h_15', 'Def Dunk Score_a', 'Def Dunk Score_h', 'Def EFG_a', 
#              'Def EFG_h', 'Def FTFGA_a', 'Def FTFGA_h', 'Def ORB_a',
#              'Def ORB_h', 'Def TOV_a', 'Def TOV_h', 'Dunk Score_a',
#              'Dunk Score_h', 'EFG_a', 'EFG_h', 'FTFGA_a', 'FTFGA_h',
#              'ORB_a', 'ORB_h', 'TOV_a', 'TOV_h', 'Win Pct_a',
#              'Win Pct_h', 'BTB_a', 'BTB_h'], 'Home Score', 'Away Score')
# print 'game accuracy:', scores_all.get_accuracy(data['Win'])

data_sample = data.sample(n=200)
scores_5_all = Game_Scores(data_sample, ['Def Dunk Score_a_5', 'Def Dunk Score_h_5', 'Def EFG_a_5',
                                  'Def EFG_h_5', 'Def FTFGA_a_5', 'Def FTFGA_h_5', 'Def ORB_a_5',
                                  'Def ORB_h_5', 'Def TOV_a_5', 'Def TOV_h_5', 'Dunk Score_a_5',
                                  'Dunk Score_h_5', 'EFG_a_5', 'EFG_h_5', 'FTFGA_a_5', 'FTFGA_h_5',
                                  'ORB_a_5', 'ORB_h_5', 'TOV_a_5', 'TOV_h_5', 'Win Pct_a_5',
                                  'Win Pct_h_5', 'BTB_a_5', 'BTB_h_5', 'Def Dunk Score_a', 'Def Dunk Score_h',
                                  'Def EFG_a',
                                  'Def EFG_h', 'Def FTFGA_a', 'Def FTFGA_h', 'Def ORB_a',
                                  'Def ORB_h', 'Def TOV_a', 'Def TOV_h', 'Dunk Score_a',
                                  'Dunk Score_h', 'EFG_a', 'EFG_h', 'FTFGA_a', 'FTFGA_h',
                                  'ORB_a', 'ORB_h', 'TOV_a', 'TOV_h', 'Win Pct_a',
                                  'Win Pct_h', 'BTB_a', 'BTB_h'],
                           'Win', 'Home Score', 'Away Score')
print 'game accuracy:', scores_5_all.get_accuracy()

rank_order = scores_5_all.get_rank_order_acc()

print rank_order
