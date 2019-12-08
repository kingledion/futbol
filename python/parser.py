#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 12:35:54 2019

@author: dhartig
"""

import csv, datetime
from teams import Team
from leagues import League, Game

def getTeamMap(filename = "/opt/futbol/data/teams.csv"):
    
    league_years = {}
    teams = {}
    
    with open(filename) as teams_in:
        
        team_rdr = csv.reader(teams_in)
        
        # Columns after the first represent years. Each team will be playing in a certain
        # league in a certain year.
        header = next(team_rdr)
        years = header[1:]
        
        # For each team, map which league they are in during each year. 
        for row in team_rdr:
            team_name = row[0]
            leagues = row[1:]
            
            # Add newly discovered teams to the set of all teams, get the team we are working on
            if team_name not in teams:
                teams[team_name] = Team(team_name)
            current_team = teams[team_name]
            
            # Add team to league for all years
            for yr, lg in zip(years, leagues):
                if (lg, yr) not in league_years:
                    league_years[(lg, yr)] = League(lg, yr)
                current_league = league_years[(lg, yr)]
                current_league.addTeam(current_team)
                
    return teams, league_years


def resolveGames(teams, leagues, filename, leaguename):
    
    def getOrExcept(group_object, name):
        try:
            return group_object[name]
        except:
            raise RuntimeError("The name {} was not initialized in getTeamMap()".format(name))
    
    with open(filename) as games_in:
        
        # Open csv reader and discard header
        game_rdr = csv.reader(games_in)
        next(game_rdr)
        
        for date, homename, awayname, homescore, awayscore in game_rdr:
            date = datetime.datetime.strptime(date, "%m/%d/%y").date()
            
            league = getOrExcept(leagues, (leaguename, "2019-2020"))
            hometeam = getOrExcept(teams, homename)
            awayteam = getOrExcept(teams, awayname)
            
            homescore = int(homescore)
            awayscore = int(awayscore)
            
            # Make this a game
            this_game = Game(date, hometeam, awayteam, homescore, awayscore)
            
            # Add game to league
            league.record(this_game)
            
                
            
            
            
            
            