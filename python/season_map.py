#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools

all_seasons = ["2014_2015", "2015_2016", "2016_2017", "2017_2018", "2018_2019", "2019_2020"]


national_leagues = {
"italy": ["serie_a", "serie_b"],
"germany": ["bdslga", "bdslga_2"],
"spain": ["la_liga", "la_liga_2"]
}

all_lgs = list(itertools.chain(*national_leagues.values()))

national_cups = {
"italy": ["coppa_italia", ]
}

league_lookup = {}
for nation in list(national_leagues.keys()) + list(national_cups.keys()):
    for lg in national_leagues.get(nation, []):
        league_lookup[lg] = nation
    for lg in national_cups.get(nation, []):
        league_lookup[lg] = nation

national_default = {
"italy": (1.00, 1.66),
"germany": (1.0, 1.5),
"spain": (1.0, 1.5)
}

def default_quality(lg, league_map):

    lg_name, lg_year = lg.name, lg.year

    prev_yr = previous_year(lg_year)
    #print("For league {} {} finding year {}".format(lg_year, lg_name, prev_yr))
    if prev_yr:
        try:
            half = lg_name not in all_lgs
            return league_map[lg_name, prev_yr].getRelegationQuality(half)
        except Exception as e:
            print(e)
    #print("returning default")
    return national_default[league_lookup[lg_name]]


def previous_year(year):

    i = all_seasons.index(year)
    if i == 0:
        return None
    else:
        return all_seasons[i-1]

season_list = national_leagues["italy"] + national_cups["italy"]
#season_list = list(itertools.chain(*(national_leagues.values() + national_cups.values()))

def remove_from_list(original_list, elements_to_remove):
    return [el for el in original_list if el not in set(elements_to_remove)]

season_map = {
"2014_2015": season_list,
"2015_2016": season_list,
"2016_2017": remove_from_list(season_list, ["serie_b"]),
"2017_2018": season_list,
"2018_2019": season_list,
"2019_2020": season_list
#"2014_2015": ["serie_a", "serie_b", "bdslga", "bdslga_2", "la_liga", "la_liga_2"],
#"2015_2016": ["serie_a", "serie_b", "bdslga", "bdslga_2", "la_liga", "la_liga_2"],
#"2016_2017": ["serie_a", "bdslga", "bdslga_2", "la_liga", "la_liga_2"],
#"2017_2018": ,
#"2018_2019": ["serie_a", "serie_b", "bdslga", "bdslga_2", "la_liga", "la_liga_2"],
#"2019_2020": ["serie_a", "serie_b", "bdslga", "bdslga_2", "la_liga", "la_liga_2"]
}
