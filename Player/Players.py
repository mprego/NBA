import pandas as pd
from Player import Player
from nba_py import player

class Players(object):
    def __init__(self, season):
        self.season = season
        self.player_list = player.PlayerList().info()
        #self.players = self.add_players()

    def add_players(self):
        players = {}
        for row in self.player_list:
            id = row['PERSON_ID']
            if row['TEAM_ID']>0:
                players[id] = Player(pid=id)
        return players

