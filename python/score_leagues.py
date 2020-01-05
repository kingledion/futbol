#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from parser_fbref import parseSeason
from model import TeamList

teamlist = TeamList()

teamlist, league, gamelist = parseSeason(teamlist)

for game in gamelist.order():
    game.record()

print(len(league.games_played))
print(len(league.games_future))

print(league)
print()
print("Current Table")
league.print_current_table()

print()
print("Predicted Final Table")
league.print_predicted_table()
