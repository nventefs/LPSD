from Multiplicative import multiplicative
import csv
import json
import os
import datetime

# converts test case number to name of json file
def test_case_to_string(test_case):
    tc = {
        1: "CVM Test Case 1 metric",
        2: "CVM Test Case 2",
        3: "CVM Test Case 3 Rev B",
        4: "CVM Test Case 4",
        5: "CVM Test Case 5",
        6: "CVM Test Case 6 Rev F",
        7: "CVM Test Case 7"
    }
    return tc.get(test_case) + "_CVMResults"

# provides csv name and json name
# TODO: Change pathing to reference pathing for scaleability
def load_test_case(test_case):
    csv_folder = "C:/Users/e1176752/Documents/VSCode/Projects/LPSD/LPSD/Archive/CSV/"
    csv_file = csv_folder + "Test Case " + str(test_case) + ".csv"
    
    json_location = "C:/Users/e1176752/Documents/VSCode/Projects/LPSD/LPSD/Archive/JSON/"

    filenames = {}

    for filename in os.listdir(json_location):
        filenames[filename] = os.path.getmtime(json_location + filename)
        
    v = list(filenames.values())
    k = list(filenames.keys())
    json_folder = json_location + (k[v.index(max(v))])
    json_file = (json_folder + "/" + test_case_to_string(test_case) + ".json")
    print("Read multiplicative data from {}".format(json_file))
    return [csv_file, json_file]

# reads in csv data and puts it into a non-searchable dictionary
# TODO: Change pathing to reference pathing for scaleability
def csv_read(csv_name):

    rows = []

    with open(csv_name, newline = '') as csvfile:
        csv_object = csv.reader(csvfile, delimiter = ',')
        for row in csv_object:
            rows.append(row)
        return rows, len(rows)

# calculates multiplicative given a test case single digit number
def calc_multi(test_case):
    if(test_case > 7 or test_case < 1):
        raise

    [csv_name, json_name] = load_test_case(test_case)
    [checkpoints, row_count] = csv_read(csv_name)

    f = open(json_name)
    data = json.load(f)

    levels = []; level_z = []; level_g = []; minwidth = {}; display_levels = {}; building_dictionary = {} 

    for i in data['levels']:
        levels.append(i['levelName'])
        level_z.append(i['elevation'])
        level_g.append(i['levelGuid'])
        minwidth[i['levelGuid']] = i["minWidth"]
        display_levels[i['levelGuid']] = [i["minWidth"], i['levelName']]
        building_dictionary[i['hostGuid']] = [i['minWidth'], i['levelGuid']]

    rows = []

    for k in range(1,row_count):   
        for i in data['points']:
            if(i['pointGuid'] == checkpoints[k][12]):
                
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
                        #W = building_dictionary[i['hostGuid']][0]
                        multi_3 = [multiplicative.eq_a(H, W, 0.38), "A"]
                    elif(i['isEdgeRectangular']):                       # Equation B
                        if(i['extendedPoint']):
                            H = level_z[len(level_z) - 1]
                        else:
                            H = i['position']['z']-level_z[len(level_z)-1]
                        W = minwidth[i['levelGuid']]
                        #W = building_dictionary[i['hostGuid']][0]
                        multi_3 = [multiplicative.eq_b(H, W, 0.38), "B"]
                    elif(i['isFaceHorizontal']):                        # Equation C
                        H = i['position']['z']
                        W = minwidth[i['levelGuid']]
                        #W = building_dictionary[i['hostGuid']][0]
                        multi_3 = [multiplicative.eq_c(H, W, 0.38), "C"]
                    elif(i['isEdgeOval']):                              # Equation D
                        if(i['levelGuid'] == level_g[len(level_g) - 1]):
                            H = i['position']['z']
                        else:
                            H = i['position']['z']-level_z[len(level_z)-1]
                        #W = building_dictionary[i['hostGuid']][0]
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
                        W = building_dictionary[i['hostGuid']][0]
                        P = float(checkpoints[k][13])
                        multi_3 = [multiplicative.eq_f(H, W, 0.38,P), "F"]
                    elif(i['isGableEaveEdge'] or i['isGableRidgeEdge'] or i['isGableRoof']): # Equation G
                        if(i['extendedPoint']):
                            H = i['position']['z']
                        else:
                            H = i['position']['z'] - level_z[len(level_z) - 1]
                        W = building_dictionary[i['hostGuid']][0]
                        P = float(checkpoints[k][13])
                        multi_3 = [multiplicative.eq_g(H, W, 0.38,P), "G"]
                    else:
                        raise
                    
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
                        W = building_dictionary[i['hostGuid']][0]
                        multi_5 = [multiplicative.eq_a(H, W, 0.38), "A"]
                    elif(i['isEdgeRectangular']):
                        if(i['extendedPoint']):
                            H = i['position']['z']
                        else:
                            H = i['position']['z']-level_z[len(level_z)-1]
                        W = building_dictionary[i['hostGuid']][0]
                        multi_5 = [multiplicative.eq_b(H, W, 0.38), "B"]
                    elif(i['isFaceHorizontal']):
                        H = i['position']['z']
                        W = building_dictionary[i['hostGuid']][0]
                        multi_5 = [multiplicative.eq_c(H, W, 0.38), "C"]
                    elif(i['isEdgeOval']):
                        H = i['position']['z']
                        W = building_dictionary[i['hostGuid']][0]
                        multi_5 = [multiplicative.eq_d(H, W, 0.38), "D"]
                    elif(i['isGableRidgeCorner'] or i['isGableEaveCorner']):
                        if(i['extendedPoint']):                                 # IF Extended
                            H = i['position']['z']                              # Height of the point
                        else: # Otherwise
                            H = i['position']['z'] - level_z[len(level_z) - 1]  # Height of the point - height of level 0
                        W = building_dictionary[i['hostGuid']][0]
                        P = float(checkpoints[k][13])                           # Pitch
                        multi_5 = [multiplicative.eq_f(H, W, 0.38, P), "F"]     # EQUATION F
                    elif(i['isGableRidgeEdge'] or i['isGableEaveEdge'] or i['isGableRoof']):
                        if(i['extendedPoint']):                                 # IF Extended
                            H = i['position']['z']                              # Height of the point
                        else:
                            H = i['position']['z'] - level_z[len(level_z) - 1]  # Height of the point - height of level 0
                        W = building_dictionary[i['hostGuid']][0]
                        P = float(checkpoints[k][13])                           # Pitch
                        multi_5 = [multiplicative.eq_g(H, W, 0.38, P), "G"]     # EQUATION G
                    else:
                        raise

                else:
                    if(i['isCorner'] or i['isEdgeRectangular']):
                        H = level_z[len(level_z)-1]
                        W = building_dictionary[i['hostGuid']][0]
                        Hf = i['position']['z'] - H
                        multi_5 = [multiplicative.eq_l(H, W, Hf), "L"]
                    else:
                        H = level_z[len(level_z)-1]
                        W = building_dictionary[i['hostGuid']][0]
                        Hf = i['position']['z'] - H
                        multi_5 = [multiplicative.eq_n(H, W, Hf), "N"]

                if(multi_3 == 1): multi_3 = [1, ""]
                if(multi_4 == 1): multi_4 = [1, ""]
                if(multi_5 == 1): multi_5 = [1, ""]
                
                # OUTPUT (COLUMN LETTER/COLUMN VALUE)
                #
                # A/1-POI | B/2-xl_x | C/3-xl_y | D/4-xl_z | E/5-json_x | F/6-json_y | G/7-json_z | 
                # H/8 GUID | I/9 xl_multi | J/10 json_multi | K/11 vscode_multi | 
                # L/12 EQ3_calc | M/13 EQ3_letter | N/14 EQ4_calc | O/15 EQ4_letter | P/16 EQ5_calc | Q/17 EQ5-letter
                row = [checkpoints[k][0], checkpoints[k][2], checkpoints[k][3], checkpoints[k][4], i['position']['x'], i['position']['y'], i['position']['z'], \
                        checkpoints[k][12], checkpoints[k][10], i['kiTotalMultiplicative'], multi_3[0]*multi_4[0]*multi_5[0], multi_3[0], multi_3[1], \
                        multi_4[0], multi_4[1], multi_5[0], multi_5[1]]
                rows.append(row)
    return rows

# checks multiplicative calculations and returns any red flag issues
def check_multi(multi):

    result = []

    for k in range(len(multi[:])):
        xl_multi    = float(multi[k][8])
        json_multi  = float(multi[k][9])
        vs_multi    = float(multi[k][10])

        xl_json_match = (json_multi * 0.95 < xl_multi) and (json_multi * 1.05 > xl_multi)
        vs_json_match = (json_multi * 0.95 < vs_multi) and (json_multi * 1.05 > vs_multi)

        result.append(xl_json_match or vs_json_match)
    
    return result
