#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv, datetime
from model import TeamList, League, GameList, Game

def parseSeason(teamlist: TeamList, filename = "../data/serie_a_2019_2020.csv", leaguename = "Serie A", leagueyear = 2020):

    league = League(leaguename, leagueyear)
    gamelist = GameList()

    with open(filename) as games_in:

        # Open csv dicitonary reader and discard header
        game_rdr = csv.reader(games_in)

        for row in game_rdr:

            try:
                gamedate, homename, homexg, score, awayxg, awayname = row[2], row[4], row[5], row[6], row[7], row[8]
            except KeyError as e:
                print(row)
                raise e


            try:
                date = datetime.datetime.strptime(gamedate, "%Y-%m-%d").date()
            except:
                continue

            hometeam = teamlist.getOrAdd(homename)
            awayteam = teamlist.getOrAdd(awayname)

            # parse scores if they exist
            try:
                homescore, awayscore = score.split('–')
                homescore, awayscore = int(homescore), int(awayscore)
            except:
                homescore = awayscore = None

            # parse home/away xg if they exist; otherwise make them None
            if homexg and awayxg:
                home_xg, away_xg = float(homexg), float(awayxg)
            else:
                home_xg = away_xg = None

            # Make this a game
            game = Game(date, league, hometeam, awayteam)
            if not (homescore is None):
                game.score(homescore, awayscore, home_xg, away_xg)

            # Add game to list of all games
            gamelist.add(game)

    return teamlist, league, gamelist
