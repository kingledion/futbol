#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from parser_fbref import parseSeason
from model import TeamList
from season_map import season_map, all_seasons

teamlist = TeamList()
lg_year = None
league_map = {}

for lg_year in all_seasons:

    for lg_name in season_map[lg_year]:
        filename = "../data/{}_{}.csv".format(lg_name, lg_year)


        teamlist, league, gamelist = parseSeason(teamlist, filename = filename, leagueyear=lg_year, leaguename=lg_name)
        league_map[(lg_name, lg_year)] = league

        for game in gamelist.order():
            game.record()
    for lg_name in season_map[lg_year]:

        league = league_map[lg_name, lg_year]

        print(league)
        print()
        print("Current Table")
        league.print_current_table()

    input()

for lg_name in season_map[lg_year]:

    league = league_map[lg_name, lg_year]
    print()
    print("Predicted Final Table")
    league.print_predicted_table()
