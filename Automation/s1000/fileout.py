import json
import csv
import test_case_to as test_case_to

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

    protected_point_dict = {}

    for terminal in json_data['terminals']:
        for point in terminal['results']['points']:
            if point['pointGuid'] not in protected_point_dict or not bool(protected_point_dict[point['pointGuid']]):
                protected_point_dict[point['pointGuid']] = point["protectedPoint"]
    
    return protected_point_dict

    #json_filepath = test_case_to.file_path("S1000 PROTECTEDPOINTS",generative=True,removing=False)
    #write_json(protected_point_dict, json_filepath)
        #print(point['pointGuid'] + " --- " + str(point["protectedPoint"]))

def compare_point_protected_values(test_case):
    try:
        json_param_file = open(test_case_to.file_path("S1000 PROTECTEDPOINTS",test_case))
    except:
        print(f"test case {test_case} failed")
        return

    official_protected_point_data = json.load(json_param_file)
    current_protected_point_dict = get_point_protected_values(test_case)
    
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
    print(f"{percent_correct}% of the points are correct")
    if len(missing_guid_list) != 0:
        print("The following pointGuids are not in the official list and must have changed:")
    for guid in missing_guid_list:
        print (guid)
    if len(incorrect_guid_list) != 0:
        print("The following pointGuids are incorrect:")
    for guid in incorrect_guid_list:
        print (guid)
