#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv, datetime
from model import TeamList, League, GameList, Game, EXTRA_LEAGUE

def parseSeason(teamlist: TeamList, filename, leaguename, leagueyear):

    league = League(leaguename, leagueyear)
    gamelist = GameList()

    with open(filename) as games_in:

        # Open csv dicitonary reader and discard header
        game_rdr = csv.reader(games_in)
        row = next(game_rdr)

        PREPEND_COL = False
        HAS_XG = False
        if row == ['Wk', 'Day', 'Date', 'Time', 'Home', 'Score', 'Away', 'Attendance', 'Venue', 'Referee', 'Match Report', 'Notes']:
            pass
        elif row == ['Wk', 'Day', 'Date', 'Time', 'Home', 'xG', 'Score', 'xG', 'Away', 'Attendance', 'Venue', 'Referee', 'Match Report', 'Notes']:
            HAS_XG = True
        elif row == ['Round', 'Wk', 'Day', 'Date', 'Time', 'Home', 'Score', 'Away', 'Attendance', 'Venue', 'Referee', 'Match Report', 'Notes']:
            PREPEND_COL = True
        else:
            raise RuntimeError("Unable to parse table with header row: {}".format(row))

        for row in game_rdr:

            HAS_POSTSEASON = False

            if HAS_XG:
                try:
                    gamedate, homename, homexg, score, awayxg, awayname = row[2], row[4], row[5], row[6], row[7], row[8]
                except KeyError as e:
                    print(row)
                    raise e
            elif PREPEND_COL:
                HAS_POSTSEASON = True
                rg_season, gamedate, homename, score, awayname = row[0], row[3], row[5], row[6], row[7]
                homexg = awayxg = None
            else:
                gamedate, homename, score, awayname = row[2], row[4], row[5], row[6]
                homexg = awayxg = None


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
                try:
                    home_xg, away_xg = float(homexg), float(awayxg)
                except:
                    print("Error in row with xg values", "/n", row)
            else:
                home_xg = away_xg = None

            # Make this a game
            lg = EXTRA_LEAGUE if HAS_POSTSEASON and rg_season != "Regular Season" else league
            game = Game(date, lg, hometeam, awayteam)
            if not (homescore is None):
                game.score(homescore, awayscore, home_xg, away_xg)

            # Add game to list of all games
            gamelist.add(game)

    return teamlist, league, gamelist
