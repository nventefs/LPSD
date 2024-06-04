import json
import csv
from pathlib import Path
import datetime

from values_from_test_case import *

NUMBER_OF_TEST_CASES = 16

RADIUS_FIELDS = ['Test Case', 'R2 Parameter', 'R2 Test Output', 'R5 Parameter', 'R5 Test Output']

#outputs the glov
def write_output_to_csv (path, dict_list):
    output_csv = open(path, "w+", newline='')
    writer = csv.DictWriter(output_csv, fieldnames=RADIUS_FIELDS)
    writer.writeheader()
    writer.writerows(dict_list)

def get_radii_dict(type, test_case):
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
    
    return {"Test Case" : test_case, "R2 Parameter": R2_expected, "R2 Test Output" : R2_result, "R5 Parameter": R5_expected, "R5 Test Output" : R5_result}

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
    dict_list = []
    radii_csv_path = output_dir / (datetime.datetime.now().strftime("%Y-%m-%d") + ".csv")

    get_point_protected_values("S1000", 1)
    for i in range(NUMBER_OF_TEST_CASES):
        dict_list.append(get_radii_dict("S1000", i + 1))
    write_output_to_csv(radii_csv_path, dict_list)