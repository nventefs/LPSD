from asyncio.windows_events import NULL
import csv
from types import NoneType
import numpy as np
import json

rows = []
row = []

def csv_read(datafile):
    with open(datafile, newline = '') as csvfile:
        csv_object = csv.reader(csvfile, delimiter = ',')
        for row in csv_object:
            rows.append(row)
        return rows

def check_point(csv_value, json_value):
    return ((float(csv_value) < float(json_value * 1.05) and float(csv_value) > float(json_value) * 0.95) or (float(csv_value) < float(json_value) + 1 and float(csv_value) > float(json_value) - 1))

def check_ki(csv_ki, json_ki):
    return ((csv_ki < json_ki * 1.02) and (csv_ki > json_ki * 0.98))

def csv_write(row):
    with open('outfile.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(row)


def row_count(csv_file):
    with open(csv_file, 'r', newline='') as csvfile:
        row_count = sum(1 for row in csvfile)
    return(row_count)


csv_name = 'Test Case - 7/Test Case 7.csv'
# Read in Andrew data as 
# ['Point #', 'Building', 'x', 'y', 'z', 'w', 'dmin', 'Max Magic Number', 'Magic Point', 'Max Reductive Factor', 'Total Reductive Factor']
checkpoints = csv_read(csv_name)
f = open('Test Case - 7/Cvm_Test_Case_7_V55_7-8-22.json')

data = json.load(f)
for k in range(1,row_count(csv_name)):     
    for i in data['points']:  
        if(check_point(checkpoints[k][2], i['position']['x']) and check_point(checkpoints[k][3], i['position']['y']) and check_point(checkpoints[k][4], i['position']['z'])):
            if(i['parentPointGuid'] == ''): # All virtual points have a parent point populated
                #print(i['position']['x'],",",i['position']['y'],",",i['position']['z'])
                #print(checkpoints[k][2],",",checkpoints[k][3],",",checkpoints[k][4])
                if(i['magicPoint'] != None):
                    row = [checkpoints[k][0],i['position']['x'],i['position']['y'],i['position']['z'], \
                        checkpoints[k][2],checkpoints[k][3],checkpoints[k][4],i['pointGuid'],checkpoints[k][7], \
                        i['kiTotalReductive'],checkpoints[k][9],check_ki(float(checkpoints[k][9]),float(i['kiTotalReductive'])),\
                            i['magicPoint']['bottomPoint']['x'], i['magicPoint']['bottomPoint']['y'], i['magicPoint']['bottomPoint']['z']]
                else:
                    row = [checkpoints[k][0],i['position']['x'],i['position']['y'],i['position']['z'], \
                    checkpoints[k][2],checkpoints[k][3],checkpoints[k][4],i['pointGuid'],checkpoints[k][7], \
                        i['kiTotalReductive'],checkpoints[k][9],check_ki(float(checkpoints[k][9]),float(i['kiTotalReductive']))]
                
                csv_write(row)
                #print(i['pointGuid'])
                #print(i['kiTotalReductive'])
                #print(check_ki(float(checkpoints[k][9]),float(i['kiTotalReductive'])))
            
        
f.close()  