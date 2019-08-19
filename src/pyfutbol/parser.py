#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 10:52:25 2019

@author: dhartig
"""

import csv, itertools, numpy as np
from definitions import DATAPATH

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)

champs_base = 260

champs_qual_score = { # nothing if you qualify for the group stage
        "Q": 0,#230, #  for participation
        "1": 0,#280, # for participation
        "2": 0,#380, # for participation
        "3": 0,#480, # for participation, but not for losers in league path
        "P": 5000, # for loss
        "L": 0 # league path loser from round 3
        }

champs_adv_score = {
        7: 15250,
        6: 15250,
        5: 15250+9500,
        4: 15250+9500+10500,
        3: 15250+9500+10500+12000,
        2: 15250+9500+10500+12000+15000,
        1: 15250+9500+10500+12000+19000,
        0: 0
        }
champs_gwin = 2700
champs_gdraw = 900

def champ_score(qual, adv, gwin, gdraw):
    qual_score = sum([champs_qual_score[q] for q in qual])
    adv_score = champs_adv_score[adv]
    base_score = qual_score if adv_score == 0 else adv_score
    return base_score + champs_gwin*gwin + champs_gdraw*gdraw

europa_qual_score = {
        "Q": 0,#220,
        "1": 0,#240,
        "2": 0,#260,
        "3": 0,#280,
        "P": 0#300
        }
europa_adv_score = {
        7: 2920,
        6: 2920+500,
        5: 2920+500+1100,
        4: 2920+500+1100+1500,
        3: 2920+500+1100+1500+2400,
        2: 2920+500+1100+1500+2400+4500,
        1: 2920+500+1100+1500+2400+8500,
        0: 0
        }
europa_gwin = 570
europa_gdraw = 190
europa_gplace = {
        1: 1000,
        2: 500,
        3: 0,
        4: 0,
        0: 0}

def europa_score(qual, adv, gwin, gdraw, gplace):
    qual_score = sum([europa_qual_score[q] for q in qual])
    adv_score = europa_adv_score[adv]
    base_score = qual_score if adv_score == 0 else adv_score
    return base_score + europa_gwin*gwin + europa_gdraw*gdraw + europa_gplace[gplace]


yr_rng = range(2019, 2005, -1)
all_data = {}

def getint(string):
    return int(string) if string != "" else 0


with open("{}/champions_data.csv".format(DATAPATH), "r") as champs_in:
    champs_rdr = csv.reader(champs_in)
    
    next(champs_rdr)
    next(champs_rdr)
    
    
    for row in champs_rdr:
        
        name = row[0]
        country = row[1]
        
        data = {"country": country}
        
        groups = grouper(row[2:], 4, 0)
        groups = [(list(q), getint(r), getint(w), getint(d)) for q, r, w, d in groups]
        
        yr = 2019 
        while len(groups) > 0:
            data[yr] = champ_score(*groups.pop(0))
            yr = yr - 1
        
        all_data[name] = data
        
with open("{}/europa_data.csv".format(DATAPATH), "r") as europa_in:
    europa_rdr = csv.reader(europa_in)
    
    next(europa_rdr)
    next(europa_rdr)
    
    
    for row in europa_rdr:
        
        name = row[0]
        country = row[1]
        
        d = {"country": country}
        
        groups = grouper(row[2:], 5, 0)
        groups = [(list(q), getint(r), getint(w), getint(d), getint(p)) for q, r, w, d, p in groups]
        
        yr = 2019 
        while len(groups) > 0:
            d[yr] = europa_score(*groups.pop(0))
            yr = yr - 1
        
        if name in all_data:
            for yr in yr_rng:
                all_data[name][yr] = all_data[name][yr] + d[yr]
        else:
            all_data[name] = d
        

country_data = {}        
        
for k, v in all_data.items():
    
    scores = [str(all_data[k].get(yr, 0)) for yr in yr_rng]
    if any([int(s) > 0 for s in scores]):
#        print(",".join([k, v['country'], *scores]))
        n_scores = np.array([int(i) for i in scores])
        country_data[v['country']] = country_data.get(v['country'], np.zeros(len(scores))) + n_scores
              
country_list = [[k, sum(v)/len(v)] + list(v) for k, v in country_data.items()]
for l in sorted(country_list, key = lambda x: x[1], reverse = True):
    print(",".join([str(i) for i in l]))


            
            
        
