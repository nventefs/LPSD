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

# Read in Andrew data as 
# ['Point #', 'Building', 'x', 'y', 'z', 'w', 'dmin', 'Max Magic Number', 'Magic Point', 'Max Reductive Factor', 'Total Reductive Factor']
checkpoints = csv_read('Test Case 1.B Floating Castle Data.csv') 

f = open('CVM_ Floating_Castles_1.B.json')
data = json.load(f)
for i in data['points']:
    print(i['position']['x'])

f.close()