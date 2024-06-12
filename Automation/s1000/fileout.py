import json
import csv
import test_case_to as test_case_to
import constants

NUMBER_OF_TEST_CASES = 16

RADIUS_FIELDS = ['Test Case', 'R2 Parameter', 'R2 Test Output', 'R5 Parameter', 'R5 Test Output']

# function to output the data from the list of dictionaries to the file at the specified path
def write_output_to_csv (path, dict_list):
    output_csv = open(path, "w", newline='')
    writer = csv.DictWriter(output_csv, fieldnames=RADIUS_FIELDS)
    writer.writeheader()
    writer.writerows(dict_list)

def write_json(data, path):
    json_file = open(path, "w")
    json.dump(data, json_file)
    json_file.close()

def read_csv(path):
    file = open(path, "r")
    dict_list = []
    reader = csv.DictReader(file)
    for row in reader:
        dict_list.append(row)
    file.close()
    return dict_list

# function to get a dictionary for the expected (parameter) values and the values from the json file for a given test case
def get_test_radius_results(json_file_path):
    #open the json file for the test case, return if it cannot be opened
    test_json_file = open(json_file_path)
    #read data
    json_data = json.load(test_json_file)
    #put data into variables
    R2_result = round(json_data['terminals'][0]['results']['R2'],2)
    R5_result = round(json_data['terminals'][0]['results']['R5'],2)
    return {"R2 Test Output" : R2_result, "R5 Test Output" : R5_result}

#Unfinished, currently just gets value of point protected for a given test case
# TODO: Make a parameters file for the point protected values and compare test values to it.
def get_point_protected_values(json_file_path):
    try:
        input_json_file = open(json_file_path)
    except:
        print(f"could not open {json_file_path}")
        return

    json_data = json.load(input_json_file)

    protected_point_dict = {}

    for terminal in json_data['terminals']:
        for point in terminal['results']['points']:
            if point['pointGuid'] not in protected_point_dict or not bool(protected_point_dict[point['pointGuid']]):
                protected_point_dict[point['pointGuid']] = point["protectedPoint"]
    
    return protected_point_dict

def compare_point_protected_values(json_param_file_path, json_current_file_path):
    try:
        json_param_file = open(json_param_file_path)
    except:
        print(f"Could not open {json_param_file_path}")
        return

    official_protected_point_data = json.load(json_param_file)
    current_protected_point_dict = get_point_protected_values(json_current_file_path)
    
    total_points = 0
    incorrect_guid_list = []
    missing_guid_list = []
    for key in current_protected_point_dict:
        if key not in official_protected_point_data:
            missing_guid_list.append(key)
        elif official_protected_point_data[key] != current_protected_point_dict[key]:
            incorrect_guid_list.append(key)
        total_points = total_points + 1
    
    percent_correct = (1 - len(incorrect_guid_list) / total_points)*100
    print(f"{percent_correct}% of the points are correct in file {json_current_file_path}")
    if len(missing_guid_list) != 0:
        print("The following pointGuids are not in the official list and must have changed:")
    for guid in missing_guid_list:
        print (guid)
    if len(incorrect_guid_list) != 0:
        print("The following pointGuids are incorrect:")
    for guid in incorrect_guid_list:
        print (guid)