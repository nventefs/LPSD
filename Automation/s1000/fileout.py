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

# writes data to a json file
# a dictionary is recommended here
def write_json(data, path):
    json_file = open(path, "w")
    json.dump(data, json_file)
    json_file.close()

# returns a list of dictionaries of each line from a csv file
def read_csv(path):
    file = open(path, "r")
    dict_list = []
    reader = csv.DictReader(file)
    for row in reader:
        dict_list.append(row)
    file.close()
    return dict_list

# function to get a dictionary for the expected (parameter) values and the values from the json file for a given test case
# used in system 1000
def get_test_radius_results(json_file_path):
    #open the json file for the test case, return if it cannot be opened
    test_json_file = open(json_file_path)
    #read data
    json_data = json.load(test_json_file)
    #put data into variables
    R2_result = round(json_data['terminals'][0]['results']['R2'],2)
    R5_result = round(json_data['terminals'][0]['results']['R5'],2)
    return {"R2 Test Output" : R2_result, "R5 Test Output" : R5_result}

# gets the protected point values from a json file and ORs multiple together if necessary
def get_point_protected_values(type, json_file_path):
    try:
        input_json_file = open(json_file_path)
    except:
        print(f"could not open {json_file_path}")
        return

    json_data = json.load(input_json_file)

    protected_point_dict = {}

    if type == "S1000":
        # use both terminals
        for terminal in json_data['terminals']:
            # loop through each point in each terminal
            for point in terminal['results']['points']:
                # if the point is not in the dictionary or is false, set the protected point to be the current protected point
                # this way, if you get a false or a true, then the value in the dictionary will be true
                if point['pointGuid'] not in protected_point_dict or not bool(protected_point_dict[point['pointGuid']]):
                    protected_point_dict[point['pointGuid']] = point["protectedPoint"]
    elif type == "S2000":
        # a bit of an odd way of doing this, but the json file went {results{longnumber{points[]}}}
        # and there was only a single long number that differs between test cases, so I needed the "first" thing in the results dict
        iter_results = iter(json_data['Results'])
        # this line is equivalent to json_data['Results'][the long number]['Points'], but is a general use across test cases
        for point in json_data['Results'][next(iter_results)]['Points']:
            # same as system 1000, only adds/updates the dict value if the point is false or isnt in it
            if point['pointGuid'] not in protected_point_dict or not bool(protected_point_dict[point['pointGuid']]):
                protected_point_dict[point['pointGuid']] = point["protectedPoint"]

    return protected_point_dict

# compares the protected point values from one json file to those in a master file with the expected protected point values
def compare_point_protected_values(type, json_param_file_path, json_current_file_path):
    # open the file with the parameters
    try:
        json_param_file = open(json_param_file_path)
    except:
        print(f"Could not open {json_param_file_path}")
        return

    # read data from parameter file
    official_protected_point_data = json.load(json_param_file)
    # read data from test results for this test case
    current_protected_point_dict = get_point_protected_values(type, json_current_file_path)
    
    total_points = 0
    incorrect_guid_list = []
    missing_guid_list = []
    for key in current_protected_point_dict:
        # if the point isnt in the parameter file, add it to the missing list
        if key not in official_protected_point_data:
            missing_guid_list.append(key)
        # if the key's true/false value is different, add it to incorrect list
        elif official_protected_point_data[key] != current_protected_point_dict[key]:
            incorrect_guid_list.append(key)
        total_points = total_points + 1
    
    # find the percent of correct points in the file
    percent_correct = round((1 - len(incorrect_guid_list) / total_points)*100,2)
    print(f"{percent_correct}% of the points are correct in file {json_current_file_path}")

    # print the missing list if there is any missing
    if len(missing_guid_list) != 0:
        print("The following pointGuids are not in the official list and must have changed:")
    for guid in missing_guid_list:
        print (guid)
   
    # print the incorrect list if there are any incorrect
    if len(incorrect_guid_list) != 0:
        print("The following pointGuids are incorrect:")
    for guid in incorrect_guid_list:
        print (guid)