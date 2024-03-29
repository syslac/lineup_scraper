from io import StringIO, BytesIO
import os

try:
    prefs = open('preferences.csv', 'r', encoding='utf-8')
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
        prefs_matrix[votes[0]] = votes[1:]

    final_band_list = []
    for band in pres:
        final_band_list.append((band.split(';'))[0])

    merged_result = open('merged_preferences.csv', 'w')
    header = header.strip()
    print(header, file = merged_result)
    i = 0
    for band in final_band_list:
        if i == 0:
            i += 1
            continue
        try:
            print(band + ';' + ';'.join(prefs_matrix[band]),file = merged_result)
        except KeyError:
            print(band + ';'*(len(header.split(';')) - 1), file = merged_result)

except IOError:
    exit('file not found')
