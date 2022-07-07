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

def check_ki(csv_ki, json_ki):
    return ((csv_ki < json_ki * 1.02) and (csv_ki > json_ki * 0.98))

def csv_write(row):
    with open('outfile.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(row)


# Read in Andrew data as 
# ['Point #', 'Building', 'x', 'y', 'z', 'w', 'dmin', 'Max Magic Number', 'Magic Point', 'Max Reductive Factor', 'Total Reductive Factor']
checkpoints = csv_read('Test Case 1.B Floating Castle Data.csv') 
f = open('CVM_ Floating_Castles_1.B.json')


data = json.load(f)
for k in range(6,48):     
    for i in data['points']:  
        if(check_point(checkpoints[k][2], i['position']['x']) and check_point(checkpoints[k][3], i['position']['y']) and check_point(checkpoints[k][4], i['position']['z'])):
            if(i['parentPointGuid'] == ''): # All virtual points have a parent point populated
                #print(i['position']['x'],",",i['position']['y'],",",i['position']['z'])
                #print(checkpoints[k][2],",",checkpoints[k][3],",",checkpoints[k][4])
                row = [i['position']['x'],i['position']['y'],i['position']['z'],checkpoints[k][2],checkpoints[k][3],checkpoints[k][4],i['pointGuid'],i['kiTotalReductive'],check_ki(float(checkpoints[k][10]),float(i['kiTotalReductive']))]
                csv_write(row)
                #print(i['pointGuid'])
                #print(i['kiTotalReductive'])
                #reductive.append(i['kiTotalReudctive'])
                #print(check_ki(float(checkpoints[k][10]),float(i['kiTotalReductive'])))
            
        
f.close()