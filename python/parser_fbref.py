#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv, datetime
from model import TeamList, League, GameList, Game, EXTRA_LEAGUE, PPG
import season_map

def parseSeason(teamlist: TeamList, gamelist: GameList, prev_leagues, filename, leaguename, leagueyear, initial = False, is_lg = True):

    league = League(leaguename, leagueyear)

    default = (PPG, PPG) if initial else season_map.default_quality(league, prev_leagues)

    with open(filename) as games_in:

        # Open csv dicitonary reader and discard header
        game_rdr = csv.reader(games_in)
        row = next(game_rdr)

        table_formats = set([])
        if row == ['Wk', 'Day', 'Date', 'Time', 'Home', 'Score', 'Away', 'Attendance', 'Venue', 'Referee', 'Match Report', 'Notes'] or \
                row == ['Round', 'Day', 'Date', 'Time', 'Home', 'Score', 'Away', 'Attendance', 'Venue', 'Referee', 'Match Report', 'Notes']:
            pass
        elif row == ['Wk', 'Day', 'Date', 'Time', 'Home', 'xG', 'Score', 'xG', 'Away', 'Attendance', 'Venue', 'Referee', 'Match Report', 'Notes']:
            table_formats = {"XG"}
        elif row == ['Round', 'Wk', 'Day', 'Date', 'Time', 'Home', 'Score', 'Away', 'Attendance', 'Venue', 'Referee', 'Match Report', 'Notes']:
            table_formats = {"Round"}
        elif row == ['Round', 'Wk', 'Day', 'Date', 'Time', 'Home', 'xG', 'Score', 'xG', 'Away', 'Attendance', 'Venue', 'Referee', 'Match Report', 'Notes']:
            table_formats = {"XG", "Round"}
        else:
            raise RuntimeError("Unable to parse table with header row: {}".format(row))

        for row in game_rdr:

            if "XG" in table_formats:
                if "Round" in table_formats:
                    rg_season, gamedate, homename, homexg, score, awayxg, awayname = row[0], row[3], row[5], row[6], row[7], row[8], row[9]
                else:
                    gamedate, homename, homexg, score, awayxg, awayname = row[2], row[4], row[5], row[6], row[7], row[8]
                    rg_season = None
            else:
                if "Round" in table_formats:
                    rg_season, gamedate, homename, score, awayname = row[0], row[3], row[5], row[6], row[7]
                    homexg = awayxg = None
                else:
                    gamedate, homename, score, awayname = row[2], row[4], row[5], row[6]
                    homexg = awayxg = rg_season = None

            if leaguename in ["champs"]:
                homename = " ".join(homename.split(" ")[:-1])
                awayname = " ".join(awayname.split(" ")[1:])


            try:
                date = datetime.datetime.strptime(gamedate, "%Y-%m-%d").date()
            except:
                continue

            hometeam = teamlist.getOrAdd(homename, default, is_lg)
            awayteam = teamlist.getOrAdd(awayname, default, is_lg)

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
            lg = EXTRA_LEAGUE if rg_season and rg_season != "Regular Season" else league
            game = Game(date, lg, hometeam, awayteam)
            if not (homescore is None):
                game.score(homescore, awayscore, home_xg, away_xg)

            # Add game to list of all games
            gamelist.add(game)

    return teamlist, league, gamelist
