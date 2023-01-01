from io import StringIO, BytesIO
from functools import reduce
import os
from pprint import pprint

def sum_convert (a, b):
    aa = 0
    bb = 0
    try:
        aa = int(a)
        bb = int(b)
    except:
        cc = 0
    return aa + bb

try:
    prefs = open('merged_preferences.csv', 'r')
    pres = open('presences.csv', 'r')

    prefs_matrix = {}
    header = prefs.readline()
    people = [] 
    for person in header.split(';'):
        if (person != ''):
            people.append(person)
    for band_line in prefs:
        band_line = band_line.strip()
        votes = band_line.split(';')
        prefs_matrix[votes[0]] = reduce(sum_convert, votes[1:], 0)

    festival_band_list = {}
    festival_header = pres.readline()
    festivals = [] 
    for fest in festival_header.split(';'):
        festivals.append(fest)
        festival_band_list[fest] = []
    for band_line in pres:
        band_line = band_line.strip()
        presences = band_line.split(';')
        for i in range(1,len(presences)):
            if (presences[i] == "1"):
                festival_band_list[festivals[i]].append((presences[0], prefs_matrix[presences[0]]))
    
    for (fest, band_list) in festival_band_list.items():
       festival_band_list[fest] = sorted(band_list, key=lambda x: x[1])
       festival_band_list[fest].reverse()

    merged_result = open('fest_lineup.csv', 'w')
    header = ";".join(festival_band_list.keys())
    print(header, file = merged_result)
    can_continue = True
    i = 0
    while can_continue:
        at_least_one_continues = False
        for (k,v) in festival_band_list.items():
            if (v != None and len(v) > i):
                print((v[i][0])+";", file = merged_result, end='')
                at_least_one_continues = True
            else:
                print(';',file=merged_result, end='')
        print("", file = merged_result)
        i = i + 1
        if at_least_one_continues:
            can_continue = True
        else:
            can_continue = False

except IOError:
    exit('file not found')
