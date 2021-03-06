#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 19:54:49 2018

@author: ZCC
"""

import hdf5_getters as GETTERS
import beat_aligned_feats as BEAT
import json
import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt

#build path file
#start with track_id selected from subset_track_metadata.db
#path format = #MillionSong/data/A/D/H/TRADHRX12903CD3866.h5
#path format = MillionSong/data/3rd/4th/5th/full.h5
file_str = 'TRBHKXX128F4252D02'
file_h5 = file_str + '.h5'
start = file_str[:2]
third = file_str[2]
fourth = file_str[3]
fifth = file_str[4]
end = file_str[5:]
path = 'data/' + str(third) + '/' + str(fourth) + '/' + str(fifth) + '/' + file_h5 

h5 = GETTERS.open_h5_file_read(path)
artist = GETTERS.get_artist_name(h5)
title = GETTERS.get_title(h5)
print('artist: ', artist, ' ', 'title: ', title)

chroma = BEAT.get_btchromas(h5)
timbre = BEAT.get_bttimbre(h5)
loudness_max = BEAT.get_btloudnessmax(h5)
chroma_loudness = BEAT.get_btchromas_loudness(h5)

#print loudness_max
#convert np array to list
chroma = chroma.tolist()
timbre = timbre.tolist()
loudness_max = loudness_max.tolist()
chroma_loudness = chroma_loudness.tolist()

#check data type
print type(loudness_max)

chroma_object = {}
for x in range(len(chroma)):
    chroma_object[x] = json.dumps((chroma[x]))

timbre_object = {}
for x in range(len(timbre)):
    timbre_object[x] = json.dumps((timbre[x]))

loudness_max_object = {}
for x in range(len(loudness_max)):
    loudness_max_object[x] = json.dumps((loudness_max[x]))

chroma_loudness_object = {}
for x in range(len(chroma_loudness)):
    chroma_loudness_object[x] = json.dumps((chroma_loudness[x]))

json_data = {}
json_data['chroma'] = chroma_object
json_data['timbre'] = timbre_object
json_data['loudness-max'] = loudness_max_object
json_data['chroma-loudness-oject'] = chroma_loudness_object


#print json_data['chroma']
print json_data.keys()
#print json.dumps(object)
        
    
    
    
