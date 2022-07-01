import csv
import numpy as np
import json

rows = []

def csv_read(datafile):
    with open(datafile, newline = '') as csvfile:
        csv_object = csv.reader(csvfile, delimiter = ',')
        for row in csv_object:
            rows.append(row)
        return rows

def check_point(csv_value, json_value):
    return ((float(csv_value) < float(json_value * 1.05) and float(csv_value) > float(json_value) * 0.95) or (float(csv_value) < float(json_value) + 1 and float(csv_value) > float(json_value) - 1))

# Read in Andrew data as 
# ['Point #', 'Building', 'x', 'y', 'z', 'w', 'dmin', 'Max Magic Number', 'Magic Point', 'Max Reductive Factor', 'Total Reductive Factor']
checkpoints = csv_read('Test Case 1.B Floating Castle Data.csv') 
print('Looking for point',checkpoints[6])
print('Looking for x value of',checkpoints[6][2])
print('Looking for y value of',checkpoints[6][3])
print('Looking for z value of',checkpoints[6][4])

f = open('CVM_ Floating_Castles_1.B.json')
data = json.load(f)
for i in data['points']:
    if(check_point(checkpoints[6][2], i['position']['x']) and check_point(checkpoints[6][3], i['position']['y']) and check_point(checkpoints[6][4], i['position']['z'])):
        print('Found csv point ', checkpoints[6])
        print('JSON value of ',i['position'])
        print(i['pointGuid'])
        
f.close()