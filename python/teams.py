#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 13:25:31 2019

@author: dhartig
"""

GAME_IMPORTANCE_FACTOR = 10
MAX_WIN = 3

class Team:
       
    def __init__(self, name):
        self.name = name
        self.rating = 0.0
        
        print("Creating new team: {}".format(self.name))
        
    def __repr__(self):
        return "Team({})".format(self.name)
    
    def __str__(self):
        return "{}: {:.2f}".format(self.name, self.rating)
    
    def score(self, game_rating):
        game_rating = max(-1*MAX_WIN, min(game_rating, MAX_WIN))
        self.rating = self.rating + game_rating / GAME_IMPORTANCE_FACTOR