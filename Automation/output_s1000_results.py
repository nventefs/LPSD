import json
import csv
from pathlib import Path
import datetime

from values_from_test_case import *

NUMBER_OF_TEST_CASES = 16
dict_list = []
FIELDS = ['Test Case', 'R2 Parameter', 'R2 Test Output', 'R5 Parameter', 'R5 Test Output']

def write_output_to_csv ():
    output_csv = open(output_dir / (datetime.datetime.now().strftime("%Y-%m-%d") + ".csv"), "w+", newline='')
    writer = csv.DictWriter(output_csv, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(dict_list)

def compare_radii_with_parameters(type, test_case):
    try:
        input_json_file = open(test_dir / test_case_to_json("S1000",test_case))
    except:
        print(f"could not open json file for case {test_case}")
        return
    
    param_csv_file = open(param_dir / "S1000 Parameters.csv")

    json_data = json.load(input_json_file)
    csv_data = csv.DictReader(param_csv_file)

    R2_result = json_data['terminals'][0]['results']['R2']
    R5_result = json_data['terminals'][0]['results']['R5']

    for line in csv_data:
        if line.get("TC") == str(test_case):
            R2_expected = line.get('R2')
            R5_expected = line.get('R5')
            break
    
    dict_list.append({"Test Case" : test_case, "R2 Parameter": R2_expected, "R2 Test Output" : R2_result, "R5 Parameter": R5_expected, "R5 Test Output" : R5_result})

def get_point_protected_values(type, test_case):
    try:
        input_json_file = open(test_dir / test_case_to_json("S1000",test_case))
    except:
        print(f"test case {test_case} failed")
        return

    json_data = json.load(input_json_file)
    for point in json_data['points']:
        print(point['pointGuid'] + " --- " + str(point["protectedPoint"]))

test_dir = generate_folder_location("S1000 TEST")
output_dir = generate_folder_location("S1000 OUTPUT")
param_dir = generate_folder_location("S1000 PARAMS")
if __name__ == '__main__':
    get_point_protected_values("S1000", 1)
    for i in range(NUMBER_OF_TEST_CASES):
        compare_radii_with_parameters("S1000", i + 1)
    write_output_to_csv()