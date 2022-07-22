from asyncio.windows_events import NULL
import csv
from types import NoneType
import numpy as np
import json
from Multiplicative import multiplicative

rows        = []
row         = []
jsonnames   = ['Cvm_Test_Case_1 Metric_V61_7-7-22', 'Cvm_Test_Case_2_V47_7-8-22', 'Cvm_Test_Case_3_RevB_V26_7-8-22',\
                'Cvm_Test_Case_4_V41_7-22-22',  'Cvm_Test_Case_5_V52_7-8-22', '', 'Cvm_Test_Case_7_V55_7-8-22']

def csv_read(datafile): # import csv file
    with open(datafile, newline = '') as csvfile:
        csv_object = csv.reader(csvfile, delimiter = ',')
        for row in csv_object:
            rows.append(row)
        return rows

def check_point(csv_value, json_value): # compare csv and json x,y,z (+/- 5% or within 1m)
    return ((float(csv_value) < float(json_value * 1.05) and float(csv_value) > float(json_value) * 0.95) or (float(csv_value) < float(json_value) + 1 and float(csv_value) > float(json_value) - 1))

def check_ki(csv_ki, json_ki): # compare csv and json ki (+/- 2%)
    return ((csv_ki < json_ki * 1.02) and (csv_ki > json_ki * 0.98))

def csv_write(row): # write the csv outfile
    with open('outfile.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(row)

def row_count(csv_file): # count total rows in csv file
    with open(csv_file, 'r', newline='') as csvfile:
        row_count = sum(1 for row in csvfile)
    return(row_count)

def test_case(i):
    csvname = 'Test Case - '+ str(i) + '/Test Case '+ str(i) +'.csv'
    jsonname = 'Test Case - '+ str(i) + '/' + jsonnames[i-1] + '.json'
    return [csvname, jsonname]


#print(multiplicative.eq_a(20.0,10.0,0.38))


# Read in Andrew data: 
# ['Point #', 'Building', 'x', 'y', 'z', 'dmin', 'Max Magic Number', 'Magic Point', 'Max Reductive Factor', 'Total Reductive Factor', 'Ki Multiplicative']
[csv_name, json_name] = test_case(1)
checkpoints = csv_read(csv_name)
f = open(json_name)
data = json.load(f)

""" for i in data['levels']:
    print(i['elevation'])
 """

for k in range(1,row_count(csv_name)):     
    for i in data['points']:  
        if(check_point(checkpoints[k][2], i['position']['x']) and check_point(checkpoints[k][3], i['position']['y']) and check_point(checkpoints[k][4], i['position']['z'])):
            if(i['parentPointGuid'] == ''): # All virtual points (manual points) have a parent point populated
                # Add .csv row [point, json x, json y, json z, xl x, xl y, xl z, pointguid, xl multi, json multi, check multi, json reduc, xl reduc, check reduc, json magic point, json mp_x, json mp_y, json mp_z]
                if(i['magicPoint'] != None):
                    row = [checkpoints[k][0],i['position']['x'],i['position']['y'],i['position']['z'], \
                        checkpoints[k][2],checkpoints[k][3],checkpoints[k][4],i['pointGuid'], \
                        checkpoints[k][10], i['kiTotalMultiplicative'],check_ki(float(checkpoints[k][10]),float(i['kiTotalMultiplicative'])),checkpoints[k][7], \
                        i['kiTotalReductive'],checkpoints[k][9],check_ki(float(checkpoints[k][9]),float(i['kiTotalReductive'])),\
                            i['magicPoint']['bottomPoint']['x'], i['magicPoint']['bottomPoint']['y'], i['magicPoint']['bottomPoint']['z']]
                else:
                # Add .csv row [point, json x, json y, json z, xl x, xl y, xl z, pointguid, xl multi, json multi, check multi, json reduc, xl reduc, check reduc]
                    row = [checkpoints[k][0],i['position']['x'],i['position']['y'],i['position']['z'], \
                    checkpoints[k][2],checkpoints[k][3],checkpoints[k][4],i['pointGuid'], \
                    checkpoints[k][10], i['kiTotalMultiplicative'],check_ki(float(checkpoints[k][10]),float(i['kiTotalMultiplicative'])),checkpoints[k][7], \
                        i['kiTotalReductive'],checkpoints[k][9],check_ki(float(checkpoints[k][9]),float(i['kiTotalReductive']))]
                
                csv_write(row)
                #print(i['pointGuid'])
                #print(i['kiTotalReductive'])
                #print(check_ki(float(checkpoints[k][9]),float(i['kiTotalReductive'])))
                #print(i['position']['x'],",",i['position']['y'],",",i['position']['z'])
                #print(checkpoints[k][2],",",checkpoints[k][3],",",checkpoints[k][4])
       
f.close() 