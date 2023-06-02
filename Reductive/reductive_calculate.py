import csv
import json
import os

# provides csv name and json name
def load_test_case(test_case):
    csvname = 'Test Case - ' + str(test_case) + '/Test Case ' + str(test_case) +'.csv'
    directory = './Test Case - ' + str(test_case) + '/'

    filenames = []
    timestamps = []

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
    print("Read data from {}".format(filenames[index]))
    return[csvname, filenames[index]]

# reads in csv data and puts it into a dictionary
def csv_read(csv_name):

    rows = []

    with open(csv_name, newline = '') as csvfile:
        csv_object = csv.reader(csvfile, delimiter = ',')
        for row in csv_object:
            rows.append(row)
        return rows, len(rows)

# checks results in the reductvie calculations given xl/json/vscode calculations and +/- tolerance 3%
def reduc_check(xl_reduc, json_reduc, vscode_reduc):
    if(((vscode_reduc>json_reduc*0.97) and (vscode_reduc<json_reduc*1.03)) or ((xl_reduc>json_reduc*0.97) and (xl_reduc<json_reduc*1.03))):
        return True
    else:
        return False

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