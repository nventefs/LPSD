from asyncio.windows_events import NULL
import csv
from types import NoneType
import numpy as np
import json
from itertools import islice

rows        = []
row         = []

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

def csv_write(row): # write the csv outfile
    with open('Results.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(row)

def compare(coord_ref, coord_0, coord_1, coord_2 = (0,0,0), coord_3 = (0,0,0), coord_4 = (0,0,0)): # compare point data of various points
    d_0 = abs(coord_ref[0] - coord_0[0]) + abs(coord_ref[1] - coord_0[1]) + abs(coord_ref[2] - coord_0[2])
    d_1 = abs(coord_ref[0] - coord_1[0]) + abs(coord_ref[1] - coord_1[1]) + abs(coord_ref[2] - coord_1[2])
    d_2 = abs(coord_ref[0] - coord_2[0]) + abs(coord_ref[1] - coord_2[1]) + abs(coord_ref[2] - coord_2[2])
    d_3 = abs(coord_ref[0] - coord_3[0]) + abs(coord_ref[1] - coord_3[1]) + abs(coord_ref[2] - coord_3[2])
    d_4 = abs(coord_ref[0] - coord_4[0]) + abs(coord_ref[1] - coord_4[1]) + abs(coord_ref[2] - coord_4[2])

    if(d_0 < d_1 and d_0 < d_2 and d_0 < d_3 and d_0 < d_4):
        return 0
    if(d_1 < d_0 and d_1 < d_2 and d_1 < d_3 and d_1 < d_4):
        return 1
    if(d_2 < d_0 and d_2 < d_1 and d_2 < d_3 and d_2 < d_4):
        return 2
    if(d_3 < d_0 and d_3 < d_1 and d_3 < d_2 and d_3 < d_4):
        return 3
    if(d_4 < d_0 and d_4 < d_1 and d_4 < d_2 and d_4 < d_3):
        return 3
    else:
        return 0

csv_name = 'outfile.csv'
infile = csv_read(csv_name)
iteration = iter(range(0,row_count(csv_name)-4))

for k in iteration:
    if(infile[k][0] == infile[k+1][0]):
        if(infile[k+1][0] == infile[k+2][0]):
            if(infile[k+2][0] == infile[k+3][0]):
                if(infile[k+3][0] == infile[k+4][0]):
                    next(islice(iteration, 4, 4), None)  
                    coord_0 = (float(infile[k][1]), float(infile[k][2]), float(infile[k][3]))
                    coord_1 = (float(infile[k+1][1]), float(infile[k+1][2]), float(infile[k+1][3]))
                    coord_2 = (float(infile[k+2][1]), float(infile[k+2][2]), float(infile[k+2][3]))
                    coord_3 = (float(infile[k+3][1]), float(infile[k+3][2]), float(infile[k+3][3]))
                    coord_4 = (float(infile[k+4][1]), float(infile[k+4][2]), float(infile[k+4][3]))
                    coord_ref = (float(infile[k][4]), float(infile[k][5]), float(infile[k][6]))

                    val = compare(coord_ref, coord_0, coord_1, coord_2, coord_3, coord_4)
                    if val == Exception:
                        print(k)
                    row = infile[k + val]

                else:
                    next(islice(iteration, 3, 3), None)  
                    coord_0 = (float(infile[k][1]), float(infile[k][2]), float(infile[k][3]))
                    coord_1 = (float(infile[k+1][1]), float(infile[k+1][2]), float(infile[k+1][3]))
                    coord_2 = (float(infile[k+2][1]), float(infile[k+2][2]), float(infile[k+2][3]))
                    coord_3 = (float(infile[k+3][1]), float(infile[k+3][2]), float(infile[k+3][3]))
                    coord_ref = (float(infile[k][4]), float(infile[k][5]), float(infile[k][6]))

                    val = compare(coord_ref, coord_0, coord_1, coord_2, coord_3)
                    if val == Exception:
                        print(k)
                    row = infile[k + val]
            else:
                next(islice(iteration, 2, 2), None)  
                coord_0 = (float(infile[k][1]), float(infile[k][2]), float(infile[k][3]))
                coord_1 = (float(infile[k+1][1]), float(infile[k+1][2]), float(infile[k+1][3]))
                coord_2 = (float(infile[k+2][1]), float(infile[k+2][2]), float(infile[k+2][3]))
                coord_ref = (float(infile[k][4]), float(infile[k][5]), float(infile[k][6]))

                val = compare(coord_ref, coord_0, coord_1, coord_2)
                if val == Exception:
                    print(k)
                row = infile[k + val]

        else:
            next(islice(iteration, 1, 1), None)  
            coord_0 = (float(infile[k][1]), float(infile[k][2]), float(infile[k][3]))
            coord_1 = (float(infile[k+1][1]), float(infile[k+1][2]), float(infile[k+1][3]))
            coord_ref = (float(infile[k][4]), float(infile[k][5]), float(infile[k][6]))
            coord = compare(coord_ref, coord_0, coord_1)

            val = compare(coord_ref, coord_0, coord_1)
            try:
                row = infile[k + val]
            except:
                row = infile[k]

    else:
        row = infile[k]    

    csv_write(row)