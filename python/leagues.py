#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 13:28:29 2019

@author: dhartig
"""

from teams import Team
from warnings import warn

HOMEFIELD_GOAL_ADV = 0.38

class Game:
    
    def __init__(self, date, hometeam, awayteam, homescore, awayscore):
        self.date = date
        self.hometeam = hometeam
        self.awayteam = awayteam
        self.homescore = homescore
        self.awayscore = awayscore
        
    def getPoints(self):
        if self.homescore > self.awayscore:
            return {self.hometeam.name: 3, self.awayteam.name: 0}
        elif self.homescore < self.awayscore:
            return {self.hometeam.name: 0, self.awayteam.name: 3}
        else:
            return {self.hometeam.name: 1, self.awayteam.name: 1}
        
    def score(self):
        
        # Get the ratings for the participating teams before the action
        homerating, awayrating = self.ratings()
         
        # Calculate the ratings for the game
        expected_pd = self.hometeam.rating + HOMEFIELD_GOAL_ADV - self.awayteam.rating
        actual_pd = self.homescore - self.awayscore
        game_diff = actual_pd - expected_pd
        
        # Adust the ratings for the inolved teams
        self.hometeam.score(game_diff)
        self.awayteam.score(game_diff * -1)
        
        # Display results
#        if actual_pd > 0:
#            fstring = "{0} ({2:.2f}) {6} defeats {1} ({3:.2f}) {7} -> {0}: {4:.2f}, {1}: {5:.2f})"
#        elif actual_pd < 0:
#            fstring = "{1} ({3:.2f}) {7} defeats {0} ({2:.2f}) {6} -> {1}: {5:.2f}, {0}: {4:.2f})"
#        else:
#            fstring = "{0} ({2:.2f}) {6} ties {1} ({3:.2f}) {7} -> {0}: {4:.2f}, {1}: {5:.2f})"
#        print(fstring.format(*self.names(), homerating, awayrating, *self.ratings(), *self.scores()))
        
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
        this_game.score()
        
        # record the game in this league
        self.games_played.append(this_game)

    def print_table(self):
        table_dict = {}
        played_dict = {}
        
        # record point for all games played
        for g in self.games_played:
            for name, pts in g.getPoints().items():
                table_dict[name] = table_dict.get(name, 0) + pts
                played_dict[name] = played_dict.get(name, 0) + 1
                
        # make list sorted by points
        table_list = [(name, pts) for name, pts in table_dict.items()]

        # add team ratingsratings
        table_list = sorted([(name, played_dict[name], pts, self.teams[name].rating) for name, pts in table_list], key = lambda tpl: (tpl[2], tpl[3]), reverse = True)
        
        # print
        for name, plyd, pts, rating in table_list:
            print("{:<25}{:<4}{:<5}".format(name, str(plyd), str(pts)), "{:5.2f}".format(rating))
        
    