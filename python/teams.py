#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 13:25:31 2019

@author: dhartig
"""

from scipy.stats import skellam, poisson
from math import pow


HOMEFIELD_GOAL_ADV = 0.38

GAME_IMPORTANCE_FACTOR = 25
MAX_POINT_DIFF = 3
PPG = 1.34

class Team:
       
    def __init__(self, name):
        self.name = name
        self.o_rating = PPG
        self.d_rating = PPG
        
        #print("Creating new team: {}".format(self.name))
        
    def __repr__(self):
        return "Team({})".format(self.name)
    
    def __str__(self):
        return "{}: {:.2f}".format(self.name, self.rating)
    
def score(hometeam, awayteam, homescore, awayscore, neutral_field = False):
    
    homefield_advantage = 0 if neutral_field else HOMEFIELD_GOAL_ADV / 2
    
    # Store prior ratings
    prior_home_ratings = (hometeam.o_rating, hometeam.d_rating)
    prior_away_ratings = (awayteam.o_rating, awayteam.d_rating)
     
    # Calculate the expected goals for the game
    home_exp = hometeam.o_rating * awayteam.d_rating / PPG + homefield_advantage
    away_exp = awayteam.o_rating * hometeam.d_rating / PPG - homefield_advantage
    
    home_adv_portion = home_exp / (home_exp + away_exp) * homefield_advantage
    
    home_exp = home_exp + home_adv_portion
    away_exp = away_exp - home_adv_portion
    
    # Calculte the difference between actual and expected goals, subject to maxima
    home_diff = max(-1*MAX_POINT_DIFF, min(MAX_POINT_DIFF, homescore - home_exp))
    away_diff = max(-1*MAX_POINT_DIFF, min(MAX_POINT_DIFF, awayscore - away_exp))

    # Adust the ratings for the inolved teams
    hometeam.o_rating = hometeam.o_rating + home_diff/GAME_IMPORTANCE_FACTOR
    hometeam.d_rating = hometeam.d_rating + away_diff/GAME_IMPORTANCE_FACTOR
    
    awayteam.o_rating = awayteam.o_rating + away_diff/GAME_IMPORTANCE_FACTOR
    awayteam.d_rating = awayteam.d_rating + home_diff/GAME_IMPORTANCE_FACTOR
    
    #     Display results
#    if homescore > awayscore:
#        fstring = "{0} ({4:.1f}, {5:.1f}) {2} defeats {1} ({6:.1f}, {7:.1f}) {3} -> {0}: ({8:.1f}, {9:.1f}), {1}: ({10:.1f}, {11:.1f})"
#    elif homescore < awayscore:
#        fstring = "{1} ({6:.1f}, {7:.1f}) {3} defeats {0} ({4:.1f}, {5:.1f}) {2} -> {0}: ({8:.1f}, {9:.1f}), {1}: ({10:.1f}, {11:.1f})"
#    else:
#        fstring = "{0} ({4:.1f}, {5:.1f}) {2} ties {1} ({6:.1f}, {7:.1f}) {3} -> {0}: ({8:.1f}, {9:.1f}), {1}: ({10:.1f}, {11:.1f})"
#    print(fstring.format(hometeam.name.upper(), awayteam.name, \
#                         homescore, awayscore, \
#                         *prior_home_ratings, *prior_away_ratings, \
#                         hometeam.o_rating, hometeam.d_rating, awayteam.o_rating, awayteam.d_rating))
#    
#    input()
        
def predict_pts(hometeam, awayteam, neutral_field = False):
    
    
    homefield_advantage = 0 if neutral_field else HOMEFIELD_GOAL_ADV / 2
    
        # Calculate the expected goals for the game
    home_exp = hometeam.o_rating * awayteam.d_rating / PPG + homefield_advantage
    away_exp = awayteam.o_rating * hometeam.d_rating / PPG - homefield_advantage
    
    home_adv_portion = home_exp / (home_exp + away_exp) * homefield_advantage
    
    home_exp = home_exp + home_adv_portion
    away_exp = away_exp - home_adv_portion
    
    # calculate chances of results
    home_win = skellam.sf(0, home_exp, away_exp)
    away_win = skellam.cdf(-1, home_exp, away_exp)
    tie = 1 - home_win - away_win
    
    
    
    return {hometeam.name: home_win*3 + tie, awayteam.name: away_win*3 + tie}