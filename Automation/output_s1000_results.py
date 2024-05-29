import json
import csv
from pathlib import Path
import datetime


NUMBER_OF_TEST_CASES = 16
dict_list = []
FIELDS = ['Test Case', 'R2 Parameter', 'R2 Test Output', 'R5 Parameter', 'R5 Test Output']

def test_case_to_json(test_case):
    return "S1000 QA TC" + str(test_case) + "_ESEResults.json"

def write_output_to_csv ():
    output_csv = open(result_dir / (datetime.datetime.now().strftime("%Y-%m-%d") + ".csv"), "w+", newline='')
    writer = csv.DictWriter(output_csv, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(dict_list)

def compare_values_with_parameters(test_case):
    global result_dir
    root_dir = Path(__file__).resolve().parent.parent
    s1000_dir = root_dir / "Archive" / "s1000"
    json_dir = s1000_dir / "JSON"
    result_dir = s1000_dir / "Results"

    folder_name = datetime.datetime.now().strftime("%Y-%m-%d")

    json_dir = json_dir / folder_name
    
    json_file = open(json_dir / test_case_to_json(test_case))
    csv_file = open(s1000_dir / "S1000 Parameters.csv")

    json_data = json.load(json_file)
    csv_data = csv.DictReader(csv_file)

    R2_result = json_data['terminals'][0].get('results').get('R2')
    R5_result = json_data['terminals'][0].get('results').get('R5')

    for line in csv_data:
        if line.get("TC") == str(test_case):
            break
    R2_expected = line.get('R2')
    R5_expected = line.get('R5')

    dict_list.append({"Test Case" : test_case, "R2 Parameter": R2_expected, "R2 Test Output" : R2_result, "R5 Parameter": R5_expected, "R5 Test Output" : R5_result})

    #print(f'R2:\nexpected {R2_expected}\nresult {R2_result}')


for i in range(6):
    compare_values_with_parameters(i+1)
write_output_to_csv()