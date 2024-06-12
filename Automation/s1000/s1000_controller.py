import threading
from get_json import get_json_s1000
import test_case_to
from fileout import *
import constants

NUMBER_OF_TESTS = 16

if __name__ == '__main__':
    threads = []
    num_threads = int(input("How many threads would you like to use? (maximum 4 recommended): "))
    total_tests_done = 0
    cycle = 0


    #Runs all 16 test cases using num_threads threads
    while True:
        for i in range(num_threads):
            threads.append(threading.Thread(target=get_json_s1000, args=(num_threads*cycle + i+1,), name=f"thread {i+1}"))
            threads[i].start()
            total_tests_done += 1
            if total_tests_done == NUMBER_OF_TESTS:
                break
        while len(threads) > 0:
            threads[0].join()
            threads.pop(0)
        cycle += 1
        if total_tests_done == NUMBER_OF_TESTS:
            break

    
    csv_results_path = constants.S1000_CURRENT_RESULTS_FILE

    for i in range(NUMBER_OF_TESTS):
        compare_point_protected_values("S1000", constants.S1000_POINT_PROTECTION_PARAM_FILE, constants.S1000_CURRENT_JSON_FOLDER / test_case_to.json_filename("S1000", i + 1))

    # gets the test case and the expected radius values for those test cases from the parameter file
    radius_dict_list = read_csv(constants.S1000_RADIUS_PARAMETER_FILE)

    # loops through each test case and adds the values from the json files to the radius dict for each test case
    # after this loop each dictionary in the dict list will have test case, expected r2 and r5, and actual r2 and r5
    for i in range(NUMBER_OF_TESTS):
        radius_dict_list[i].update(get_test_radius_results(constants.S1000_CURRENT_JSON_FOLDER / test_case_to.json_filename("S1000", i + 1)))

    write_output_to_csv(csv_results_path, radius_dict_list)