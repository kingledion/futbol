#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scipy.stats import skellam
from statistics import mean

HOMEFIELD_GOAL_ADV = 0.38

GAME_IMPORTANCE_FACTOR = 25
MAX_POINT_DIFF = 3
PPG = 1.34


class Game:

    def __init__(self, date, league, hometeam, awayteam, neutral_field = False):
        # ensure datetime
        self.date = date

        self.league = league

        # ensure both are Team objects
        if type(hometeam) is not Team or type(awayteam) is not Team:
            raise RuntimeError("Attempting to initialize game with non-Team")
        self.hometeam = hometeam
        self.awayteam = awayteam

        self.homescore = self.awayscore = self.home_xg = self.away_xg = None

        self.neutral_field = neutral_field

    def __repr__(self):
        return "{}: {} @ {}".format(self.date.strftime("%m/%d/%y"), self.hometeam.name, self.awayteam.name)

#    def asTuple(self):
#        return self.hometeam, self.awayteam, self.homescore, self.awayscore, self.neutral_field

    def getPoints(self):
        if self.homescore == None:
            return None
        if self.homescore > self.awayscore:
            return {self.hometeam.name: 3, self.awayteam.name: 0}
        elif self.homescore < self.awayscore:
            return {self.hometeam.name: 0, self.awayteam.name: 3}
        else:
            return {self.hometeam.name: 1, self.awayteam.name: 1}

    def hasScore(self):
        return not self.homescore is None

    def score(self, homescore, awayscore, home_xg = None, away_xg = None):

        # ensure neither are None
        self.homescore = homescore
        self.awayscore = awayscore

        # ensure both or neither are None
        self.home_xg = home_xg
        self.away_xg = away_xg

    def record(self, display = False):

        if self.hasScore():


            hometeam = self.hometeam
            awayteam = self.awayteam

            home_score = mean([self.homescore, self.home_xg]) if self.home_xg else self.homescore
            away_score = mean([self.awayscore, self.away_xg]) if self.away_xg else self.awayscore

            homefield_advantage = 0 if self.neutral_field else HOMEFIELD_GOAL_ADV / 2

            # Store prior ratings
            if display == True:
                prior_home_ratings = (hometeam.o_rating, hometeam.d_rating)
                prior_away_ratings = (awayteam.o_rating, awayteam.d_rating)

            # Calculate the expected goals for the game
            home_exp = hometeam.o_rating * awayteam.d_rating / PPG + homefield_advantage
            away_exp = awayteam.o_rating * hometeam.d_rating / PPG - homefield_advantage

            home_adv_portion = home_exp / (home_exp + away_exp) * homefield_advantage

            home_exp = home_exp + home_adv_portion
            away_exp = away_exp - home_adv_portion

            # Calculte the difference between actual and expected goals, subject to maxima
            home_diff = max(-1*MAX_POINT_DIFF, min(MAX_POINT_DIFF, home_score - home_exp))
            away_diff = max(-1*MAX_POINT_DIFF, min(MAX_POINT_DIFF, away_score - away_exp))

            # Adust the ratings for the inolved teams
            hometeam.o_rating = hometeam.o_rating + home_diff/GAME_IMPORTANCE_FACTOR
            hometeam.d_rating = hometeam.d_rating + away_diff/GAME_IMPORTANCE_FACTOR

            awayteam.o_rating = awayteam.o_rating + away_diff/GAME_IMPORTANCE_FACTOR
            awayteam.d_rating = awayteam.d_rating + home_diff/GAME_IMPORTANCE_FACTOR

            if display == True:
               if self.homescore > self.awayscore:
                   fstring = "{0} ({4:.1f}, {5:.1f}) {2} defeats {1} ({6:.1f}, {7:.1f}) {3} -> {0}: ({8:.1f}, {9:.1f}), {1}: ({10:.1f}, {11:.1f})"
               elif self.homescore < self.awayscore:
                   fstring = "{1} ({6:.1f}, {7:.1f}) {3} defeats {0} ({4:.1f}, {5:.1f}) {2} -> {0}: ({8:.1f}, {9:.1f}), {1}: ({10:.1f}, {11:.1f})"
               else:
                   fstring = "{0} ({4:.1f}, {5:.1f}) {2} ties {1} ({6:.1f}, {7:.1f}) {3} -> {0}: ({8:.1f}, {9:.1f}), {1}: ({10:.1f}, {11:.1f})"
               print(fstring.format(hometeam.name.upper(), awayteam.name, \
                                    self.homescore, self.awayscore, \
                                    *prior_home_ratings, *prior_away_ratings, \
                                    hometeam.o_rating, hometeam.d_rating, awayteam.o_rating, awayteam.d_rating))

               input()

        self.league.add(self)


    def predict(self):

        hometeam = self.hometeam
        awayteam = self.awayteam

        homefield_advantage = 0 if self.neutral_field else HOMEFIELD_GOAL_ADV / 2

            # Calculate the expected goals for the game
        home_exp = hometeam.o_rating * awayteam.d_rating / PPG + homefield_advantage
        away_exp = awayteam.o_rating * hometeam.d_rating / PPG - homefield_advantage

        home_adv_portion = home_exp / (home_exp + away_exp) * homefield_advantage

        home_exp = home_exp + home_adv_portion
        away_exp = away_exp - home_adv_portion

        # calculate chances of results
        home_win = skellam.sf(0, home_exp, away_exp)
        away_win = skellam.cdf(-1, home_exp, away_exp)
        tie = 1 - home_win - away_win

        return {hometeam.name: home_win*3 + tie, awayteam.name: away_win*3 + tie}

class GameList:

    def __init__(self):
        self.games = []

    def add(self, *games: Game):
        self.games.extend(games)

    def order(self):
        return sorted(self.games, key = lambda g: g.date)

class Team:

    def __init__(self, name, off_rating = None, def_rating = None):
        self.name = name
        self.o_rating = PPG if off_rating is None else off_rating
        self.d_rating = PPG if def_rating is None else def_rating

        #print("Creating new team: {}".format(self.name))

    def __repr__(self):
        return "Team({})".format(self.name)

    def __str__(self):
        return self.name

class TeamList:

    def __init__(self, *teams):
        self.teams = {t.name: t for t in teams}

    def _add(self, teamname):
        self.teams[teamname] = Team(teamname)
        print("Added new team {}".format(teamname))

    def getOrAdd(self, teamname):
        if teamname not in self.teams:
            self._add(teamname)
        return self.teams[teamname]

class League:

    def __init__(self, name, year):
        self.name = name
        self.year = year
        self.teamlist = {}
        self.games_played = []
        self.games_future = []

        print("Initialized a new league:", self)

    def getLeagueQuality(self):

        offense = [team.o_rating for team in self.teamlist]
        defense = [team.d_rating for team in self.teamlist]

        return mean(offense), mean(defense)

    def _addTeams(self, *newteams):
        for team in newteams:
            if team.name not in self.teamlist:
                self.teamlist[team.name] = team
                #print("Added {} to {}".format(team, self))


    def __repr__(self):
        return "League({}, {})".format(self.name, self.year)

    def __str__(self):
        return "{} {}".format(self.year, self.name)

    def add(self, game):
        self._addTeams(game.hometeam, game.awayteam)
        if game.hasScore():
            self.games_played.append(game)
        else:
            self.games_future.append(game)

    def print_current_table(self):
        o_ratings, d_ratings = {tm.name: tm.o_rating for tm in self.teamlist.values()}, {tm.name: tm.d_rating for tm in self.teamlist.values()}
        diff_ratings = {tm.name: tm.o_rating - tm.d_rating for tm in self.teamlist.values()}
        print_table(*self.get_points(), o_ratings, d_ratings, diff_ratings)

    def get_points(self):
        table_dict = {}
        played_dict = {}

        # record point for all games played
        for g in self.games_played:
            for name, pts in g.getPoints().items():
                table_dict[name] = table_dict.get(name, 0) + pts
                played_dict[name] = played_dict.get(name, 0) + 1
        return table_dict, played_dict

    def print_predicted_table(self):

        table, played = self.get_points()

        for game in self.games_future:
            for name, pts in game.predict().items():
                table[name] = table.get(name, 0) + pts
                played[name] = played.get(name, 0) + 1

        table = {k: int(round(v)) for k, v in table.items()}
        print_table(table, played)

        # An old way of predicting a table for home/away leagues
        # table_dict, played_dict = self.get_points()
        #
        # team_set = set(self.teams.keys())
        #
        # completed_game_tree = {}
        # for g in self.games_played:
        #     completed_game_tree[g.hometeam.name] = completed_game_tree.get(g.hometeam.name, set([])) | {g.awayteam.name}
        #
        # for home_tm in team_set:
        #     prev_opps = completed_game_tree.get(home_tm, set({}))
        #
        #     tm_results = [predict_pts(self.teams[home_tm], self.teams[away_tm]) for away_tm in team_set if away_tm not in prev_opps | {home_tm}]
        #
        #     for rslt in tm_results:
        #         for name, pts in rslt.items():
        #             table_dict[name] = table_dict.get(name, 0) + pts
        #             played_dict[name] = played_dict.get(name, 0) + 1
        #
        # table_dict = {k: int(round(v)) for k, v in table_dict.items()}
        #
        # print_table(table_dict, played_dict)


def print_table(table_dict, played_dict, *ratings):

    # make list sorted by points
    table_list = [(name, pts) for name, pts in table_dict.items()]

    # add team ratingsratings
    table_list = sorted([(name, played_dict[name], pts) for name, pts in table_list], key = lambda tpl: (tpl[2]), reverse = True)

    # print
    row_format = "{:<25}{:<4}{:<5}" + "{:5.1f}"*len(ratings)
    for name, plyd, pts in table_list:
        row_vals = [name, str(plyd), str(pts)] + [rating_col[name] for rating_col in ratings]
        print(row_format.format(*row_vals))

EXTRA_LEAGUE = League("Extra", "All_years")
