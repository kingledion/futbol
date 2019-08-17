#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 14:02:53 2019

@author: dhartig
"""

import csv, itertools, numpy as np

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)

def getint(string):
    return int(string) if string != "" else 0

def getshares(league, cup): 
    lg_share = 2 if league > 0 else 0
    chmp_share = 3 if league == 1 else 0
    return lg_share + chmp_share + cup

def getscore(league, cup):
    lg_share = max(11 - int(league), 2) if league > 0 else 0
    chmp_share = 2 if league == 1 else 0
    return int((lg_share/2 + chmp_share + cup)*2)

yr_rng = range(2019, 2005, -1)
all_data = {}


with open("./league_standing.csv", "r") as league_in:
    league_rdr = csv.reader(league_in)
    
    next(league_rdr)
    next(league_rdr)
    
    for row in league_rdr:
        
        name = row[0]
        country = row[1]
        
        for row in league_rdr:
        
            name = row[0]
            country = row[1]
            
            data = {"country": country}
            
            groups = grouper(row[2:], 2, 0)
            groups = [(getint(l), getint(c)) for l, c in groups]
            
            yr = 2019 
            while len(groups) > 0:
                data[yr] = getscore(*groups.pop(0))
                yr = yr - 1
            
            all_data[name] = data
            
for k, v in all_data.items():
    
    scores = [str(all_data[k].get(yr, 0)) for yr in yr_rng]
    if any([float(s) > 0 for s in scores]):
        print(",".join([k, v['country'], *scores]))           
