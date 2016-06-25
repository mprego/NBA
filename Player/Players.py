import pandas as pd
from Player import Player
from nba_py import player

class Players(object):
    def __init__(self, season, test_size = -1):
        self.season = season
        self.player_list = player.PlayerList().info()
        if test_size != -1:
            self.player_list = self.player_list.ix[0:test_size,:]
        self.players = self.add_players()

    def add_players(self):
        players = {}
        for index, row in self.player_list.iterrows():
            id = row['PERSON_ID']
            if row['TEAM_ID']>0:
                players[id] = Player(pid=id)
        return players

