import csv
import json
import os
import datetime
import math
import numpy as np
import matplotlib 

global E_p
global Q
global e_b
global k_v

E_p = 8.85e-12                          # Permittivity of free space
h = 5000                                # Base cloud height (5000m)
e_0 = 3.1e6                             # Default breakdown of electric field 3.1MV/m
Q = {                                   # Charge based on LPL
        1: 0.16,
        2: 0.38,
        3: 0.93,
        4: 1.8
    }        
k_v = {
        1: 1.1,
        2: 1.1,
        3: 1.075,
        4: 1.05
    }    

# Determines striking distance based on Ki value [DONE]
def striking_distance(Ki, LPL, SE):
    e_b = e_0 * (0.82 + 0.18 * ( 1 - 0.5 * SE/1000))    # This might be missing from LPSD 4.0
    E_up = e_b/Ki
    d = 0.5
    z = np.arange(0,1000,0.1) # striking distance range from 0 to 1000 (ds_max)

    # ELECTRIC FIELD CALCULATIONS
    EA_1 = np.array((Q.get(LPL) / (math.pi * E_p * (h - z) ** 2)))
    EA_2 = np.array(h / d - z / d) / ((1 + (z / d) ** 2) ** 0.5)
    EA = []
    EA_E_up = []
    for k in range(len(EA_1)):
        EA.append(EA_1[k] * (EA_2[k] + math.asinh(z[k] / d) - math.asinh(h/d)))
        EA_E_up.append(abs(EA[k]-E_up))
    
    index_min = np.argmin(EA_E_up)

    if z[index_min] < 0.1:
        print("Striking distance is zstep or 0.1")
    else:
        print("Striking distance is equal to: {} m".format(z[index_min]))
    return z[index_min]

def z_m(H, LPL, SE, ds):
    """
    Calculations for CVM Down - This finds the minimum point on the second plot and extracts the z value that it corresponds to. 
    This approximates the striking distance to the nearest zstep (0.1m). zstep value here is defaulted to 0.1 m because typical 
    values for dist are significantly larger than 0.1 m. Eup measures the effective e-field value that must be attained for an 
    upward leader to form from the POI.
    """

    z_max = 8       # maximum meters for z_m values
    z_step = 0.01
    z = np.arange(0,z_max,z_step)

    e_b = e_0 * (0.82 + 0.18 * ( 1 - 0.5 * SE/1000))    # This might be missing from LPSD 4.0

    np.seterr(invalid = 'ignore', divide='ignore')      # turn off divide by zero and invalid value errors
    E_B0 = np.array( (Q.get(LPL) / (math.pi * E_p * ((h - z) ** 2))) * ( ((h - z) / z) + np.log(z/h)))
    E_B = np.nan_to_num(E_B0, nan=np.inf)               # handle NaN values
    index_min = np.argmin(np.abs(E_B - e_b))
    E_Bmin = np.min(np.abs(E_B - e_b))
    
    z_m = z[index_min]
    
    """
    Calculations for CVM UP -  This finds the minimum point on the second plot and extracts the z value that it corresponds to. 
    This approximates zm to the nearest zstep (0.01m). zstep is defaulted here to 0.01m because zm is commonly less than 1m and 
    rounding to the nearest 0.1m doesn't provide smooth results.
    """

    
    z_up = np.arange(H,5*H,z_step)
    z_0 = np.round((k_v.get(LPL) * H - z_m * (k_v.get(LPL) - 1)) / ((k_v.get(LPL) + 1) + 0.01), 2)
    
    x_step = 0.01
    x = np.arange(z_0, H, z_step)

    d_h = np.round((z_m * (k_v.get(LPL) + 1) + H) / k_v.get(LPL), 2)
    print("d_h is equal to {}".format(d_h))
    """
    s = np.arange(-ds, ds, x_step)

    # Setting up drawing for striking distance curve and velocity driven boundary
    d_b = np.array((((z_m * (k_v.get(LPL) - 1) + z) / k_v.get(LPL)) ** 2 - (z - H) ** 2) ** 0.5 ) # positive solid blue curve
    d_r = np.array((((z_m * (k_v.get(LPL) - 1) + x) / k_v.get(LPL)) ** 2 - (x - H) ** 2) ** 0.5 ) # positive solid blue curve

    d_b_neg = d_b * -1 # negative solid blue curve
    d_r_neg = d_r * -1 # negative solid red curve
    
    sdc = np.array((ds ** 2 - s ** 2) + H) # solid red curve
    """

    if ds < d_h:
        print("ds > d_h")
        z_r = H         # height of intersection between both curves
        r_a = ds        # attractive radius is set to striking distance
        #y_max = 2*H
    elif ds > 5 * H:
        print("ds > 5*H")
        z_r = 5 * H
        r_a = (((z_m * (k_v.get(LPL) - 1) + (5 * H)) / k_v.get(LPL)) ** 2 - (4 * H) ** 2) ** 0.5            
        #y_max = np.max(sdc)
    else: 
        z_r = k_v.get(LPL) * ds - z_m * (k_v.get(LPL) - 1)
        r_a = ((ds ** 2) - (z_r - H) ** 2) ** 0.5
        #y_max = np.max(sdc)

    print("z_m = {}, height of intersection = {}, attractive radius = {}, kv = {}".format(z_m, z_r, r_a, k_v.get(LPL)))





    #z_m = z[index_min]
    return 

def cvm(LPL):
    E_p = 8.85e-12  # permittivity of free space
    Q = {           # charge based on LPL (dictionary | LPL:Q)
        1: 0.16,
        2: 0.38,
        3: 0.93,
        4: 1.8
    }
    k_v = {         # k_v based on LPL (dictionary | LPL:k_v)
        1: 1.1,
        2: 1.1,
        3: 1.075,
        4: 1.05
    }

    E_p = 8.85e-12  # permittivity of free space
    h = 5000        # cloudbase height
    Se = 0          # site elevation
    E_0 = 3.1e6     # default breakdown of electric field (3.1MV/m)

    K_v = k_v.get(LPL) # velocity ratio basedon LPL

    # Establish breakdown field value accounting for site elevation (Se)
    # At a site elevation of 0m, the breakdown field value remains the default value
    e_b = E_0 * (0.82 + 0.18 * (1 - 0.5 * (Se/1000)))

    #TODO: Add Ki calculation here (multiplicative | reductive)
    Ki = 1.4
    
    E_UP = e_b /Ki
    d_s_max = 1000  # upper range of striking distance modeling in meters
    d_s_step = 0.1  # step value for striking distance iteration
    d_a = 0.5       # standard distance to the side of POI for calculations
    z_d = range(0, d_s_max, d_s_step)   # range for striking distance modeling

    EA_1 = (Q.get(LPL)/(math.pi()*E_p*(h-z_d)**2))
    EA_2 = ((h/d_a) - (z_d/d_a) ) / ((1 + (z_d / d_a) ** 2) ** 0.5)

    EA = EA_1 * (EA_2 * math.asinh(z_d / d_a) - math.asinh(h / d_a))
    [EA_min, index] = math.min(math.abs(EA - E_UP))

#TODO: write multiplicative and reductive parts for AT... whew...
def ki(data):
    print('pewpew')

#TODO: everything
def csv_read(csv_name):

    rows = []

    with open(csv_name, newline = '') as csvfile:
        csv_object = csv.reader(csvfile, delimiter = ',')
        for row in csv_object:
            rows.append(row)
        return rows, len(rows)
    
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

def load_test_case(test_case):

    csv_folder = "C:/Users/e1176752/Documents/VSCode/Projects/LPSD/LPSD/Archive/AT/"
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

#striking_distance(137.56, 1, 0)
#TODO: determine ki, height of attractive radius, derating angle, attractive radius
# Completed: striking distance
z_m(34.28, 1, 0, striking_distance(125, 1, 0))