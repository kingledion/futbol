#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 14:00:10 2019

@author: dhartig
"""

from parser import getTeamMap, resolveGames

teams, league_years = getTeamMap()

#resolveGames(teams, league_years, "/opt/futbol/data/epl_games.csv", "Premier League")
#resolveGames(teams, league_years, "/opt/futbol/data/lga_games.csv", "La Liga")
#resolveGames(teams, league_years, "/opt/futbol/data/bnd_games.csv", "Bundesliga")
resolveGames(teams, league_years, "/opt/futbol/data/sra_games.csv", "Serie A")

yrs_to_use = [
#        "Premier League",
#        "La Liga",
#        "Bundesliga",
        "Serie A"
        ]

for lg in league_years.values():
    if lg.name in yrs_to_use:
        print()
        print("Current Table")
        
        lg.print_current_table()

for lg in league_years.values():
    if lg.name in yrs_to_use:
        print()
        print("Predicted Final Table")
        
        lg.print_predicted_table()