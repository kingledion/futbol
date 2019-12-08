#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 13:28:29 2019

@author: dhartig
"""

from teams import Team, score, predict_pts
from warnings import warn

class Game:
    
    def __init__(self, date, hometeam: Team, awayteam: Team, homescore, awayscore, neutral_field = False):
        self.date = date
        self.hometeam = hometeam
        self.awayteam = awayteam
        self.homescore = homescore
        self.awayscore = awayscore
        self.neutral_field = neutral_field
        
    def __repr__(self):
        return "{} {}, {} {}".format(self.hometeam.name, self.homescore, self.awayteam.name, self.awayscore)
    
    def asTuple(self):
        return self.hometeam, self.awayteam, self.homescore, self.awayscore, self.neutral_field
        
    def getPoints(self):
        if self.homescore > self.awayscore:
            return {self.hometeam.name: 3, self.awayteam.name: 0}
        elif self.homescore < self.awayscore:
            return {self.hometeam.name: 0, self.awayteam.name: 3}
        else:
            return {self.hometeam.name: 1, self.awayteam.name: 1}
        
#    def score(self):

        
    def names(self):
        return self.hometeam.name, self.awayteam.name
        
    def ratings(self):
        return self.hometeam.rating, self.awayteam.rating
    
    def scores(self):
        return self.homescore, self.awayscore

class League:
    
    def __init__(self, name, year):
        self.name = name
        self.year = year
        self.teams = {}
        self.games_played = []
        
        print("Creating new league: {}, {}".format(self.year, self.name))
        
    def addTeam(self, team: Team):
        if type(team) is Team:
            self.teams[team.name] = team
        else:
            warn("Attempting to add a non-Team object to League")
            
    def __repr__(self):
        return "League({}, {})".format(self.name, self.year)
    
    def __str__(self):
        return "{} {}".format(self.year, self.name)
    
    def record(self, this_game: Game):
        
        # score this game, adjusting team ratings
        score(*this_game.asTuple())
        
        # record the game in this league
        self.games_played.append(this_game)
        
    def print_current_table(self):
        o_ratings, d_ratings = {tm.name: tm.o_rating for tm in self.teams.values()}, {tm.name: tm.d_rating for tm in self.teams.values()}
        print_table(*self.get_points(), o_ratings, d_ratings)

    def get_points(self):
        table_dict = {}
        played_dict = {}
        
        # record point for all games played
        for g in self.games_played:
            for name, pts in g.getPoints().items():
                table_dict[name] = table_dict.get(name, 0) + pts
                played_dict[name] = played_dict.get(name, 0) + 1
        return table_dict, played_dict
            
    def print_predicted_table(self):
        
        table_dict, played_dict = self.get_points()
        
        team_set = set(self.teams.keys())
        
        completed_game_tree = {}
        for g in self.games_played:
            completed_game_tree[g.hometeam.name] = completed_game_tree.get(g.hometeam.name, set([])) | {g.awayteam.name}
            
        for home_tm, prev_opps in completed_game_tree.items():

            tm_results = [predict_pts(self.teams[home_tm], self.teams[away_tm]) for away_tm in team_set if away_tm not in prev_opps | {home_tm}]
                
            for rslt in tm_results:
                for name, pts in rslt.items():
                    table_dict[name] = table_dict.get(name, 0) + pts
                    played_dict[name] = played_dict.get(name, 0) + 1
                    
        table_dict = {k: int(round(v)) for k, v in table_dict.items()}
                    
        print_table(table_dict, played_dict)
            
            
def print_table(table_dict, played_dict, *ratings):
            
    # make list sorted by points
    table_list = [(name, pts) for name, pts in table_dict.items()]

    # add team ratingsratings
    table_list = sorted([(name, played_dict[name], pts) for name, pts in table_list], key = lambda tpl: (tpl[2]), reverse = True)
    
    # print
    row_format = "{:<25}{:<4}{:<5}" + "{:5.2f}"*len(ratings)
    for name, plyd, pts in table_list:
        row_vals = [name, str(plyd), str(pts)] + [rating_col[name] for rating_col in ratings]
        print(row_format.format(*row_vals))
        
                
                
        
    