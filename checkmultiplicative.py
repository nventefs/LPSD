from Multiplicative import multiplicative
from asyncio.windows_events import NULL
import csv
from types import NoneType
import numpy as np
import json

rows        = []
row         = []
jsonnames   = ['Cvm_Test_Case_1 Metric_V61_7-7-22', 'Cvm_Test_Case_2_V47_7-8-22', 'Cvm_Test_Case_3_RevB_V26_7-8-22',\
                'Cvm_Test_Case_4_V41_7-22-22',  'Cvm_Test_Case_5_V52_7-8-22', '', 'Cvm_Test_Case_7_V55_7-8-22']

# IMPORTANT: prior to running checkmultiplicative, run checkreductive and add GUID values into CSV file

def min_width(level_guid): 
    x = []
    y = []
    x_min = []
    y_min = []
    for i in data['points']:
        if(i['parentPointGuid'] == ''):
            if(i['levelGuid'] == level_guid):
                x.append(i['position']['x'])
                y.append(i['position']['y'])

    if x:
        x_min = (max(x) - min(x))
    if y:
        y_min = (max(y) - min(y))
    if x_min:
        if(x_min < y_min): 
            #print(x_min)
            return x_min
        else:
            #print(y_min)
            return y_min
    else:
        #print(y_min)
        return y_min

def csv_read(datafile): # import csv file
    with open(datafile, newline = '') as csvfile:
        csv_object = csv.reader(csvfile, delimiter = ',')
        for row in csv_object:
            rows.append(row)
        return rows

def row_count(csv_file): # count total rows in csv file
    with open(csv_file, 'r', newline='') as csvfile:
        row_count = sum(1 for row in csvfile)
    return(row_count)

def test_case(i):
    csvname = 'Test Case - '+ str(i) + '/Test Case '+ str(i) +'.csv'
    jsonname = 'Test Case - '+ str(i) + '/' + jsonnames[i-1] + '.json'
    return [csvname, jsonname]

# Read in Andrew data: 
# ['Point #', 'Building', 'x', 'y', 'z', 'dmin', 'Max Magic Number', 'Magic Point', 'Max Reductive Factor', 'Total Reductive Factor', 'Ki Multiplicative','Multiplicative Eq']
[csv_name, json_name] = test_case(1)
checkpoints = csv_read(csv_name)
f = open(json_name)
data = json.load(f)

levels              = []
level_z             = []
level_g             = []
level_min_width     = []
x                   = []
y                   = []

for i in data['levels']:
    levels.append(i['levelName'])
    level_z.append(i['elevation'])
    level_g.append(i['levelGuid'])
"""
for k in level_g:
    print(k)
    #level_min_width.append(min_width(k))
    print(min_width(k)) 
"""
#min_width(level_g[0])
#print(level_g[0])
#print(levels)
#print(level_g)
#print(level_min_width)


#print(levels)
#print(level_z)
#print(level_g)
#print(min_width("6fc52480-a9fb-4be7-9c1f-d8bb797b0c5e")) 
#for k in range(1,row_count(csv_name)): 
#    print(checkpoints[k][11])



for k in range(1,row_count(csv_name)):   
    for i in data['points']:
        if(i['pointGuid'] == checkpoints[k][12]):
            print(i['pointGuid'])
            multi_3 = 1
            multi_4 = 1
            multi_5 = 1
            if(i['levelGuid'] != level_g[len(level_g)-1] and not(i['extendedPoint'])):
                #Equation 3
                if(i['isCorner']): # Equation A
                    #print("A")
                    H = i['position']['z']-level_z[len(level_z)-1]
                    W = min_width(i['levelGuid'])
                    multi_3 = multiplicative.eq_a(H, W, 0.38)
                elif(i['isEdgeRectangular']): # Equation B
                    print("B")
                    H = i['position']['z']-level_z[len(level_z)-1]
                    W = min_width(i['levelGuid'])
                    multi_3 = multiplicative.eq_b(H, W, 0.38)
                elif(i['isFaceHorizontal']): # Equation C
                    print("C")
                    H = i['position']['z']
                    W = min_width(i['levelGuid'])
                    multi_3 = multiplicative.eq_c(H, W, 0.38)
                elif(i['isEdgeOval']): # Equation D
                    print("D")
                    H = i['position']['z']-level_z[len(level_z)-1]
                    W = min_width(i['levelGuid'])
                    multi_3 = multiplicative.eq_b(H, W, 0.38)
                else: # Equation E
                    print("E")
                    H = i['position']['z']
                    W = min_width(i['levelGuid'])
                    multi_3 = multiplicative.eq_c(H, W, 0.38)

                #Equation 4
                if(i['isCorner']):
                    print("Q")
                    multi_4 = multiplicative.eq_q(i['position']['z'])
                elif(i['isEdgeOval'] or i['isEdgeRectangular']):
                    print("R")
                    multi_4 = multiplicative.eq_r()
                else:
                    print("S")
                    multi_4 = multiplicative.eq_s(i['position']['z'])
                    
            #Equation 5
            if (i['levelGuid'] == level_g[len(level_g)-1] or i['extendedPoint']):
                if(i['isCorner']):
                    print("A")
                    H = i['position']['z']
                    W = min_width(i['levelGuid'])
                    multi_5 = multiplicative.eq_a(H, W, 0.38)
                elif(i['isEdgeRectangular']):
                    print("B")
                    H = i['position']['z']
                    W = min_width(i['levelGuid'])
                    multi_5 = multiplicative.eq_b(H, W, 0.38)
                elif(i['isFaceHorizontal']):
                    print("C")
                    H = i['position']['z']
                    W = min_width(i['levelGuid'])
                    multi_5 = multiplicative.eq_c(H, W, 0.38)
                elif(i['isEdgeOval']):
                    print("D")
                    H = i['position']['z']
                    W = min_width(i['levelGuid'])
                    multi_5 = multiplicative.eq_d(H, W, 0.38)
                else:
                    print("E")
                    H = i['position']['z']
                    W = min_width(i['levelGuid'])
                    multi_5 = multiplicative.eq_e(H, W, 0.38)
            else:
                if(i['isCorner'] or i['isEdgeRectangular']):
                    print("L") # figure this one out separately
                else:
                    print("N")

f.close()