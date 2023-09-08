import csv
import json
import datetime
import os

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
    print("Read reductive data from {}".format(json_file))
    return [csv_file, json_file]

# reads in csv data and puts it into a dictionary
# TODO: Change pathing to reference pathing for scaleability
def csv_read(csv_name):

    rows = []

    with open(csv_name, newline = '') as csvfile:
        csv_object = csv.reader(csvfile, delimiter = ',')
        for row in csv_object:
            rows.append(row)
        return rows, len(rows)

# checks results in the reductvie calculations given reductive calculations and +/- tolerance 5%
def check_reduc(reduc):

    result = []

    for k in range(len(reduc[:])):
        xl_reduc    = float(reduc[k][9])
        json_reduc  = float(reduc[k][10])
        vs_reduc    = float(reduc[k][11])

        xl_json_match = (json_reduc * 0.95 < xl_reduc) and (json_reduc * 1.05 > xl_reduc)
        vs_json_match = (json_reduc * 0.95 < vs_reduc) and (json_reduc * 1.05 > vs_reduc)

        result.append(xl_json_match or vs_json_match)
    
    return result

# calculates reductive based on incoming json, checks against existing csv in Archive/CSV
def calc_reduc(test_case):
    if(test_case > 7 or test_case < 1):
        raise
    [csv_name, json_name] = load_test_case(test_case)
    [checkpoints, row_count] = csv_read(csv_name)

    f = open(json_name)
    data = json.load(f)

    rows = []

    for k in range(1,row_count):   
        for i in data['points']:
            if(i['pointGuid'] == checkpoints[k][12]):
                    if(i['magicPoint'] != None): # reductive only applies if point has a magic point assigned to it
                        xl_reduc = float(checkpoints[k][9])
                        # reductive calculation: 0.9 * ((z_mp-z_poi)^0.51) * ((sqrt((x_mp-x_poi)^2 + (y_mp-y_poi)^2)^-0.35))                        
                        vscode_reduc = 0.9 * (i['magicPoint']['position']['z'] - i['position']['z']) ** 0.51 \
                            * (((i['magicPoint']['position']['x'] - i['position']['x']) ** 2 + (i['magicPoint']['position']['y'] - i['position']['y']) ** 2) ** 0.5) ** -0.35
                        json_reduc = i['kiTotalReductive']     
                                           
                        # OUTPUT (COLUMN LETTER/COLUMN VALUE)
                        #
                        # A/1-POI | B/2-xl_x | C/3-xl_y | D/4-xl_z | E/5-json_x | F/6-json_y | G/7-json_z | 
                        # H/8 GUID | I/9 mp_GUID | J/10 xl_reduc | K/11 json_reduc | L/12 vscode_reduc |
                        row = [checkpoints[k][0], checkpoints[k][2],checkpoints[k][3],checkpoints[k][4], \
                                i['position']['x'],i['position']['y'],i['position']['z'],i['pointGuid'], i['magicPoint']['pointGuid'],\
                                checkpoints[k][9], i['kiTotalReductive'], vscode_reduc]
                        #, reduc_check(xl_reduc, json_reduc, vscode_reduc)
                        
                        rows.append(row)
                    else:
                        xl_reduc = float(checkpoints[k][9])
                        vscode_reduc = 1
                        json_reduc = i['kiTotalReductive']  
                        row = [checkpoints[k][0], checkpoints[k][2],checkpoints[k][3],checkpoints[k][4], \
                                i['position']['x'],i['position']['y'],i['position']['z'],i['pointGuid'], "",\
                                checkpoints[k][9], i['kiTotalReductive'], vscode_reduc]
                        #, reduc_check(xl_reduc, json_reduc, vscode_reduc)
                        rows.append(row)

    return(rows)