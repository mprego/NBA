# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 20:08:14 2016

@author: Matt
"""

import pandas as pd
from ELO import ELO

schedule = pd.DataFrame(dict(Date={0: '1/1/2000', 1: '1/2/2000', 2: '1/2/2000', 3: '1/3/2000'},
                                     Home={0: 'SA', 1: 'SA', 2: 'HOU', 3: 'DAL'},
                                     Away={0: 'HOU', 1: 'CLE', 2: 'CLE', 3: 'SA'},
                                     h_score={0: 10, 1: 19, 2: 6, 3: 21},
                                     a_score={0: 9, 1: 20, 2: 10, 3: 18}))
elo = ELO(schedule, 'Date', 'Home', 'Away', 'h_score', 'a_score')
elo.create_elo(1500, 20)