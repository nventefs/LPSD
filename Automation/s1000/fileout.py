import json
import csv
from pathlib import Path
import datetime

import test_case_to as test_case_to

NUMBER_OF_TEST_CASES = 16

RADIUS_FIELDS = ['Test Case', 'R2 Parameter', 'R2 Test Output', 'R5 Parameter', 'R5 Test Output']

# function to output the data from the list of dictionaries to the file at the specified path
def write_output_to_csv (path, dict_list):
    output_csv = open(path, "w", newline='')
    writer = csv.DictWriter(output_csv, fieldnames=RADIUS_FIELDS)
    writer.writeheader()
    writer.writerows(dict_list)

# function to get a dictionary for the expected (parameter) values and the values from the json file for a given test case
def get_radii_dict(test_case):
    #open the json file for the test case, return if it cannot be opened
    test_json_file = open(test_case_to.file_path("S1000 TEST",test_case))
    param_csv_file = open(test_case_to.file_path("S1000 PARAMS"))

    #read data
    json_data = json.load(test_json_file)
    csv_data = csv.DictReader(param_csv_file)

    #put data into variables
    R2_result = json_data['terminals'][0]['results']['R2']
    R5_result = json_data['terminals'][0]['results']['R5']
    for line in csv_data:
        if line.get("TC") == str(test_case):
            R2_expected = line.get('R2')
            R5_expected = line.get('R5')
            break
    
    return {"Test Case" : test_case, "R2 Parameter": R2_expected, "R2 Test Output" : R2_result, "R5 Parameter": R5_expected, "R5 Test Output" : R5_result}

#Unfinished, currently just gets value of point protected for a given test case
# TODO: Make a parameters file for the point protected values and compare test values to it.
def get_point_protected_values(test_case):
    try:
        input_json_file = open(test_case_to.file_path("S1000 TEST",test_case))
    except:
        print(f"test case {test_case} failed")
        return

    json_data = json.load(input_json_file)
    for point in json_data['points']:
        print(point['pointGuid'] + " --- " + str(point["protectedPoint"]))


if __name__ == '__main__':
    dict_list = []
    radii_csv_path = test_case_to.file_path("S1000 OUTPUT", generative=True, removing=True)

    get_point_protected_values(1)
    for i in range(NUMBER_OF_TEST_CASES):
        dict_list.append(get_radii_dict(i + 1))
    write_output_to_csv(radii_csv_path, dict_list)