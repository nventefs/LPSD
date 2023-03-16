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
[csv_name, json_name] = test_case(7)
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
guid_investigate = "88afb1c7-1193-488d-b5ec-31dbd3651350"
POI_investigate = 12    

for k in range(1,row_count(csv_name)):   
    for i in data['points']:
        if(i['pointGuid'] == checkpoints[k][12]):
            #print(i['pointGuid'])
            multi_3 = 1.0
            multi_4 = 1.0
            multi_5 = 1.0
            if(i['levelGuid'] != level_g[len(level_g)-1] and not(i['extendedPoint'])): # IF not level 0 AND not extended 
                #Equation 3
                if(i['isCorner']):                                  # Equation A
                    if(i['extendedPoint']):
                        H = level_z[len(level_z) - 1]
                    else:
                        H = i['position']['z']-level_z[len(level_z)-1]
                    W = minwidth[i['levelGuid']]
                    multi_3 = [multiplicative.eq_a(H, W, 0.38), "A"]
                elif(i['isEdgeRectangular']):                       # Equation B
                    if(i['extendedPoint']):
                        H = level_z[len(level_z) - 1]
                    else:
                        H = i['position']['z']-level_z[len(level_z)-1]
                    W = minwidth[i['levelGuid']]
                    multi_3 = [multiplicative.eq_b(H, W, 0.38), "B"]
                elif(i['isFaceHorizontal']):                        # Equation C
                    H = i['position']['z']
                    W = minwidth[i['levelGuid']]
                    multi_3 = [multiplicative.eq_c(H, W, 0.38), "C"]
                elif(i['isEdgeOval']):                              # Equation D
                    if(i['levelGuid'] == level_g[len(level_g) - 1]):
                        H = i['position']['z']
                    else:
                        H = i['position']['z']-level_z[len(level_z)-1]
                    W = minwidth[i['levelGuid']]
                    multi_3 = [multiplicative.eq_d(H, W, 0.38), "D"]
                #else:                                           # Equation E
                #    H = i['position']['z']
                #    W = minwidth[i['levelGuid']]
                #    multi_3 = [multiplicative.eq_e(H, W, 0.38), "E"]
                elif(i['isGableEaveCorner'] or i['isGableRidgeCorner']): # Equation F
                    if(i['extendedPoint']):
                        H = i['position']['z']
                        print("this never happens")
                    else:
                        H = i['position']['z'] - level_z[len(level_z) - 1]
                    W = minwidth[level_g[(len(level_g) - 1)]]
                    P = float(checkpoints[k][13])
                    multi_3 = [multiplicative.eq_f(H, W, 0.38,P), "F"]
                elif(i['isGableEaveEdge'] or i['isGableRidgeEdge'] or i['isGableRoof']): # Equation G
                    if(i['extendedPoint']):
                        H = i['position']['z']
                    else:
                        H = i['position']['z'] - level_z[len(level_z) - 1]
                    W = minwidth[level_g[(len(level_g) - 1)]]
                    P = float(checkpoints[k][13])
                    multi_3 = [multiplicative.eq_g(H, W, 0.38,P), "G"]
                else:
                    raise
                
                if(i['pointGuid'] == guid_investigate):
                    print("POI {} H:{}, W:{}".format(POI_investigate, H,W))
                    print("POI {} is extended: {}".format(POI_investigate, i['extendedPoint']))

                #Equation 4
                if(i['isCorner'] or i['isGableEaveCorner'] or i['isGableRidgeCorner']):
                    multi_4 = [multiplicative.eq_q(0.05), "Q"]
                elif(i['isEdgeOval'] or i['isEdgeRectangular'] or i['isGableEaveEdge'] or i['isGableRidgeEdge'] or i['isGableRoof']):
                    multi_4 = [multiplicative.eq_r(), "R"]
                else:
                    multi_4 = [multiplicative.eq_s(0.05), "S"]
                    
            #Equation 5
            if (i['levelGuid'] == level_g[len(level_g)-1] or i['extendedPoint']):
                if(i['isCorner']):
                    if(i['extendedPoint']):
                        H = i['position']['z']
                    else:
                        H = i['position']['z']-level_z[len(level_z)-1]
                    W = minwidth[i['levelGuid']]
                    multi_5 = [multiplicative.eq_a(H, W, 0.38), "A"]
                elif(i['isEdgeRectangular']):
                    if(i['extendedPoint']):
                        H = level_z[len(level_z) - 1]
                    else:
                        H = i['position']['z']-level_z[len(level_z)-1]
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
                    if(i['extendedPoint']):                                 # IF Extended
                        H = i['position']['z']                              # Height of the point
                    else: # Otherwise
                        H = i['position']['z'] - level_z[len(level_z) - 1]  # Height of the point - height of level 0
                    W = minwidth[level_g[(len(level_g) - 1)]]               # Minimum width of level 0
                    P = float(checkpoints[k][13])                           # Pitch
                    multi_5 = [multiplicative.eq_f(H, W, 0.38, P), "F"]     # EQUATION F
                elif(i['isGableRidgeEdge'] or i['isGableEaveEdge'] or i['isGableRoof']):
                    if(i['extendedPoint']):                                 # IF Extended
                        H = i['position']['z']                              # Height of the point
                    else:
                        H = i['position']['z'] - level_z[len(level_z) - 1]  # Height of the point - height of level 0
                    W = minwidth[level_g[(len(level_g) - 1)]]               # Minimum width of level 0
                    P = float(checkpoints[k][13])                           # Pitch
                    multi_5 = [multiplicative.eq_g(H, W, 0.38, P), "G"]     # EQUATION G
                else:
                    raise

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

            if(i['pointGuid'] == guid_investigate):
                print("POI {}, {} is extended:{}".format(POI_investigate, i['pointGuid'], i['extendedPoint']))
                print("POI {} H:{}, W:{}, Rc:0.38".format(POI_investigate, H,W))
                print("POI Slope: {}".format(i['slope']))

                quit()

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