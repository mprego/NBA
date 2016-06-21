from nba_py import team
import pandas as pd
import time
import os.path

class Schedule(object):
    '''
    Produces an object that returns schedules and stats of NBA games
    '''

    def __init__(self, b_dt, e_dt='1/1/2020'):
        self.b_dt = pd.to_datetime(b_dt)
        self.e_dt = pd.to_datetime(e_dt)
        self.filename = self.get_filename()

        if b_dt is not None:
            self.season_name = self.get_season_name()
            self.team_list = self.get_team_list()

            if os.path.isfile(self.filename):
                self.games = pd.read_csv(self.filename)
            else:
                self.games = self.pull_games(self.b_dt, self.e_dt)
            self.games.to_csv(self.filename, index = False)

    def get_filename(self):
        start = str(self.b_dt.year) + '_' + str(self.b_dt.month) + '_' + str(self.b_dt.day)
        end = str(self.e_dt.year) + '_' + str(self.e_dt.month) + '_' + str(self.e_dt.day)
        filename = start + '-' + end + '_games.csv'
        return filename

    def get_games(self):
        return self.games

    def get_team_list(self):
        return self.team_list

    def get_season_name(self):
        # If month is October or later, then season starts this year
        if self.b_dt.month >= 10:
            year = self.b_dt.year
        else:
            year = self.b_dt.year - 1

        return str(year) + '-' + str(year + 1)[2:4]

    def get_team_list(self):
        year = self.season_name[0:4]
        team_list = team.TeamList().info()
        team_list = team_list[team_list['MAX_YEAR'] >= year].reset_index(drop=True)
        team_list = team_list[team_list['MIN_YEAR'] <= year].reset_index(drop=True)
        return team_list

    def pull_games(self, b_dt, e_dt):
        games = pd.DataFrame()
        for index, tm in self.team_list.iterrows():
            log = team.TeamGameLogs(team_id=tm['TEAM_ID'], season = self.season_name)
            games = games.append(log.info())
        games = games.reset_index(drop=True)

        for index, game in games.iterrows():
            splits = game['MATCHUP'].split(' ')
            if splits[1] == '@':
                games.set_value(index, 'Away Team', splits[0])
                games.set_value(index, 'Home Team', splits[2])
            else:
                games.set_value(index, 'Home Team', splits[0])
                games.set_value(index, 'Away Team', splits[2])
            if splits[0] == games.ix[index, 'Home Team']:
                games.set_value(index, 'Home Stats', 1)
            else:
                games.set_value(index, 'Home Stats', 0)
        h_games = games[games['Home Stats'] == 1]
        a_games = games[games['Home Stats'] == 0]

        all_games = pd.merge(h_games, a_games, on='Game_ID', suffixes=['_home', '_away']).reset_index(drop=True)
        all_games['GAME_DATE'] = pd.to_datetime(all_games['GAME_DATE_home'])
        all_games['H_WL'] = [1 if x=='W' else 0 for x in all_games['WL_home']]
        all_games['A_WL'] = [1 if x == 'L' else 0 for x in all_games['WL_home']]
        all_games = all_games.rename(index = str, columns = {'Game_ID_home':'Game_ID', 'Home Team_home':'Home Team', 'Away Team_home':'Away Team', 'PTS_home':'H_PTS', 'PTS_away':'A_PTS', 'AST_home': 'H_AST', 'AST_away':'A_AST', 'STL_home':'H_STL', 'STL_away':'A_STL', 'BLK_home': 'H_BLK', 'BLK_away':'A_BLK'})
        all_games['Pts_diff'] = [x-y for x,y in zip(all_games['H_PTS'], all_games['A_PTS'])]
        all_games = all_games[['GAME_DATE', 'Game_ID', 'H_WL', 'A_WL', 'Home Team', 'Away Team', 'H_PTS', 'A_PTS', 'Pts_diff', 'FGM_home', 'FG3M_home', 'FGA_home', 'OREB_home', 'DREB_away', 'TOV_home', 'FTM_home', 'FTA_home', 'FGM_away', 'FG3M_away', 'FGA_away', 'OREB_away',
                                             'DREB_home', 'TOV_away', 'FTM_away', 'FTA_away', 'H_AST', 'A_AST', 'H_STL', 'A_STL', 'H_BLK', 'A_BLK']]

        all_games = all_games[all_games['GAME_DATE'] >= b_dt]
        all_games = all_games[all_games['GAME_DATE'] <= e_dt]

        return all_games



    def add_four_factors(self):
        self.games = self.add_four_factors_helper(self.games, 'H_FF_', 'FGM_home', 'FG3M_home', 'FGA_home', 'OREB_home', 'DREB_away', 'TOV_home', 'FTM_home', 'FTA_home')
        self.games = self.add_four_factors_helper(self.games, 'A_FF_', 'FGM_away', 'FG3M_away', 'FGA_away', 'OREB_away',
                                             'DREB_home', 'TOV_away', 'FTM_away', 'FTA_away')
        self.games.to_csv(self.filename, index=False)
        return self.games

    def add_four_factors_helper(self, games, sfx, fgm, threepa, fga, oreb, o_drb, to, ftm, fta):
        efg = '{0}EFG'.format(sfx)
        orb = '{0}ORB'.format(sfx)
        ftfga = '{0}FTFGA'.format(sfx)
        tov = '{0}TOV'.format(sfx)

        games[efg] = [(a + .5 * b) / c for a, b, c in zip(games[fgm], games[threepa], games[fga])]
        games[orb] = [a*1.0 / (a + b) for a, b in zip(games[oreb], games[o_drb])]
        games[ftfga] = [a*1.0 / b for a, b in zip(games[ftm], games[fga])]
        games[tov] = [a / (b + .44 * c - d + a) for a, b, c, d in zip(games[to], games[fga], games[fta], games[oreb])]
        return games

    def add_dunk_data(self, log = False):
        # Need to test some stuff.  possibly just pull once for each team
        self.games = self.add_dunk_data_helper('H_', self.games, 'Team_ID_home', log)  #home team might be wrong
        self.games = self.add_dunk_data_helper('A_', self.games, 'Team_ID_away', log)  # home team might be wrong
        self.games.to_csv(self.filename, index=False)
        return self.games

    def add_dunk_data_helper(self, sfx, games, teamid, log = False):
        for index, game in self.games.iterrows():
            dunks = team.TeamShootingSplits(team_id = self.games.ix[index, teamid], season = self.season_name, date_from = self.games.ix[index, 'GAME_DATE'], date_to = self.games.ix[index, 'GAME_DATE'])
            data = dunks.shot_type_summary()
            data = data[data['GROUP_VALUE'].isin(
                ['Dunk Shot', 'Putback Dunk Shot', 'Putback Slam Dunk Shot', 'Slam Dunk Shot'])]
            score = 2 * data['FGM'].sum() - data['FGA'].sum()
            games.set_value(index, (sfx + 'dunk_made'), data['FGM'].sum())
            games.set_value(index, (sfx + 'dunk_miss'), data['FGA'].sum() - data['FGM'].sum())
            games.set_value(index, (sfx + 'dunk_score'), score)
            if log == True:
                if index%50 == 0:
                    print 'Game ' + str(index) + ' of ' + str(len(self.games))
                    print 'Saving Checkpoint...'
                    games.to_csv(self.filename, index=False)
                    print 'Sleeping for 5 minutes...'
                    time.sleep(60 * 5)
                    print "And we're back"
        return games


