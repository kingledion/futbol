#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 14:00:10 2019

@author: dhartig
"""

from parser import getTeamMap, resolveGames

teams, league_years = getTeamMap()

resolveGames(teams, league_years)

print()
for lg in league_years.values():
    lg.print_table()