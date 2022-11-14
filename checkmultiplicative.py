from Multiplicative import multiplicative
from asyncio.windows_events import NULL
import csv
from types import NoneType
import numpy as np
import json
import os
from tabulate import tabulate

#from checkreductive import minWidth

# IMPORTANT: prior to running checkmultiplicative, run checkreductive and add GUID values into CSV file
filenames           = []
timestamps          = []
levels              = []
level_z             = []
level_g             = []
rows                = []
row                 = []
minwidth            = {}
display_levels      = {}
jsonnames           = ['Cvm_Test_Case_1 Metric_V87_10-11-22', 'Cvm_Test_Case_2_V48_9-26-22', 'Cvm_Test_Case_3_RevB_V26_9-26-22',\
                        'Cvm_Test_Case_4_V41_9-26-22',  'Cvm_Test_Case_5_V53_9-26-22', 'Cvm_Test_Case_6_Rev_F_V20_10-27-22', 'Cvm_Test_Case_7_V55_9-26-22']

def min_width(level_guid): 
    #print(level_guid)
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

def min_width2(level_guid):
    print("a")


def csv_read(datafile): # import csv file
    with open(datafile, newline = '') as csvfile:
        csv_object = csv.reader(csvfile, delimiter = ',')
        for row in csv_object:
            rows.append(row)
        return rows

def csv_write(row): # write the csv outfile
    with open('outfile.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(row)

def row_count(csv_file): # count total rows in csv file
    with open(csv_file, 'r', newline='') as csvfile:
        row_count = sum(1 for row in csvfile)
    return(row_count)


def test_case(i):
    csvname = 'Test Case - ' + str(i) + '/Test Case ' + str(i) +'.csv'
    directory = './Test Case - ' + str(i) + '/'
    global filenames
    global timestamps

    for filename in os.listdir(directory):
        if(filename.endswith('.json')):
            f = os.path.join(directory, filename)
            filenames.append(f)
            d = os.path.getmtime(f)
            timestamps.append(str(d))

    for j in range(len(filenames)):
        index = j
        try:
            if timestamps[j + 1] > timestamps[j]:
                index = j + 1
        except:
            index = j
    print("Running multiplicative check on {}".format(filenames[index]))
    return[csvname, filenames[index]]

# Read in Andrew data: 
# ['Point #', 'Building', 'x', 'y', 'z', 'dmin', 'Max Magic Number', 'Magic Point', 'Max Reductive Factor', 'Total Reductive Factor', 'Ki Multiplicative','Multiplicative Eq']
[csv_name, json_name] = test_case(1)
checkpoints = csv_read(csv_name)
f = open(json_name)
data = json.load(f)

for i in data['levels']:
    levels.append(i['levelName'])
    level_z.append(i['elevation'])
    level_g.append(i['levelGuid'])
    minwidth[i['levelGuid']] = i["minWidth"]
    display_levels[i['levelGuid']] = [i["minWidth"], i['levelName']]

#print(levels)
#print(level_g)
#print(level_z)


for k in range(1,row_count(csv_name)):   
    for i in data['points']:
        if(i['pointGuid'] == checkpoints[k][12]):
            #print(i['pointGuid'])
            multi_3 = 1
            multi_4 = 1
            multi_5 = 1
            if(i['levelGuid'] != level_g[len(level_g)-1] and not(i['extendedPoint'])):
                #Equation 3
                if(i['isCorner']): # Equation A
                    H = i['position']['z']-level_z[len(level_z)-1]
                    W = minwidth[i['levelGuid']]
                    multi_3 = [multiplicative.eq_a(H, W, 0.38), "A"]
                elif(i['isEdgeRectangular']): # Equation B
                    if(i['extendedPoint']):
                        H = i['position']['z']-level_z[len(level_z)-1]
                    else:
                        H = level_z[len(level_z) - 1]
                    W = minwidth[i['levelGuid']]
                    multi_3 = [multiplicative.eq_b(H, W, 0.38), "B"]
                elif(i['isFaceHorizontal']): # Equation C
                    H = i['position']['z']
                    W = minwidth[i['levelGuid']]
                    multi_3 = [multiplicative.eq_c(H, W, 0.38), "C"]
                elif(i['isEdgeOval']): # Equation D
                    if(i['levelGuid'] == level_g[len(level_g) - 1]):
                        H = i['position']['z']
                    else:
                        H = i['position']['z']-level_z[len(level_z)-1]
                    W = minwidth[i['levelGuid']]
                    multi_3 = [multiplicative.eq_d(H, W, 0.38), "D"]
                else: # Equation E
                    H = i['position']['z']
                    W = minwidth[i['levelGuid']]
                    multi_3 = [multiplicative.eq_e(H, W, 0.38), "E"]

                #Equation 4
                if(i['isCorner']):
                    multi_4 = [multiplicative.eq_q(0.05), "Q"]
                elif(i['isEdgeOval'] or i['isEdgeRectangular']):
                    multi_4 = [multiplicative.eq_r(), "R"]
                else:
                    multi_4 = [multiplicative.eq_s(0.05), "S"]
                    
            #Equation 5
            if (i['levelGuid'] == level_g[len(level_g)-1] or i['extendedPoint']):
                if(i['isCorner']):
                    H = i['position']['z']
                    W = minwidth[level_g[len(level_g)-1]]
                    multi_5 = [multiplicative.eq_a(H, W, 0.38), "A"]
                elif(i['isEdgeRectangular']):
                    H = i['position']['z']
                    #W = minwidth[i['levelGuid']]
                    W = minwidth[level_g[len(level_g)-1]]
                    multi_5 = [multiplicative.eq_b(H, W, 0.38), "B"]
                elif(i['isFaceHorizontal']):
                    H = i['position']['z']
                    W = minwidth[i['levelGuid']]
                    multi_5 = [multiplicative.eq_c(H, W, 0.38), "C"]
                elif(i['isEdgeOval']):
                    H = i['position']['z']
                    W = minwidth[i['levelGuid']]
                    multi_5 = [multiplicative.eq_d(H, W, 0.38), "D"]
                elif(i['isGableRidgeCorner'] or i['isGableEaveCorner']):
                    H = i['position']['z']
                    W = minwidth[i['levelGuid']]
                    multi_5 = [multiplicative.eq_e(H, W, 0.38), "F"]
                else:
                    H = i['position']['z']
                    W = minwidth[i['levelGuid']]
                    multi_5 = [multiplicative.eq_e(H, W, 0.38), "G"]
            else:
                if(i['isCorner'] or i['isEdgeRectangular']):
                    H = level_z[len(level_z)-1]
                    W = minwidth[level_g[len(level_g)-1]]
                    Hf = i['position']['z'] - H
                    multi_5 = [multiplicative.eq_l(H, W, Hf), "L"]
                else:
                    H = level_z[len(level_z)-1]
                    W = minwidth[level_g[len(level_g)-1]]
                    Hf = i['position']['z'] - H
                    multi_5 = [multiplicative.eq_n(H, W, Hf), "N"]

            if(multi_3 == 1): multi_3 = [1, ""]
            if(multi_4 == 1): multi_4 = [1, ""]
            if(multi_5 == 1): multi_5 = [1, ""]
            
            row = [checkpoints[k][0], checkpoints[k][2], checkpoints[k][3], checkpoints[k][4], i['position']['x'], i['position']['y'], i['position']['z'], \
                    checkpoints[k][12], checkpoints[k][10], i['kiTotalMultiplicative'], multi_3[0]*multi_4[0]*multi_5[0], multi_3[0], multi_3[1], \
                    multi_4[0], multi_4[1], multi_5[0], multi_5[1], i['levelGuid']]
            csv_write(row)

for k in level_g:
    print('GUID : {}, Values : {}'.format(k, display_levels[k]))

f.close()