#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 14:00:10 2019

@author: dhartig
"""

from parser import getTeamMap, resolveGames

teams, league_years = getTeamMap()

resolveGames(teams, league_years)


for lg in league_years.values():
    print()
    print("Current Table")
    
    lg.print_current_table()

for lg in league_years.values():
    print()
    print("Predicted Final Table")
    
    lg.print_predicted_table()