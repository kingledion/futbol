#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

from parser_fbref import parseSeason
from model import TeamList, GameList
import season_map

def main():
    teamlist = TeamList()
    lg_year = None
    league_map = {}

    for lg_year in season_map.all_seasons:

        gamelist = GameList()

        for lg_name in season_map.season_map[lg_year]:
            filename = "../data/{}_{}.csv".format(lg_name, lg_year)

            #print(lg_year, season_map.all_seasons[0], lg_year == season_map.all_seasons[0])
            #print(lg_name, lg_name in season_map.all_lgs)

            initial = lg_year == season_map.all_seasons[0] and lg_name in season_map.all_lgs
            #print("initial: ", initial)

            teamlist, league, gamelist = parseSeason(teamlist, gamelist, league_map, filename = filename, leagueyear=lg_year, leaguename=lg_name, initial= initial, is_lg = lg_name in season_map.all_lgs)
            league_map[(lg_name, lg_year)] = league

        for game in gamelist.order():
            game.record()

        #print_all_leagues(lg_year, league_map, season_map)
        print_team_list(teamlist)


    # for lg_name in season_map.season_map[lg_year]:
    #
    #     if lg_name in season_map.all_lgs:
    #
    #         league = league_map[lg_name, lg_year]
    #         print()
    #         print("Predicted Final Table")
    #         league.print_predicted_table()
    #
    #         print()
    #         print(league.getRelegationQuality())

def print_team_list(teamlist):

    ordered_teams = sorted(teamlist.teams.values(), key = lambda tm: tm.o_rating / tm.d_rating, reverse=True)[:50]
    print()
    for tm in ordered_teams:
        str_fmt = "{:<25}" + "{:5.1f}"*3
        print(str_fmt.format(tm.name, tm.o_rating, tm.d_rating, math.log(tm.o_rating / tm.d_rating)))

    input()

def print_all_leagues(lg_year, league_map, season_map):
        for lg_name in season_map.season_map[lg_year]:
            if lg_name in season_map.all_lgs:
            #if lg_name in ["serie_a", "bdslga", "la_liga", "eng_prem"]:

                league = league_map[lg_name, lg_year]

                print(league)
                print()
                print("Current Table")
                league.print_current_table()

        input()

main()
