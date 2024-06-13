import threading
from get_json import get_json_s1000
import test_case_to
from fileout import *
import constants
import os
import time

NUMBER_OF_TESTS = 16

if __name__ == '__main__':
    threads = []
    tests_to_run = []
    in_progress = []
    num_threads = int(input("How many threads would you like to use? (maximum 4 recommended): "))
    total_tests_done = 0

    for i in range (NUMBER_OF_TESTS):
        test_case_file_path = constants.S1000_CURRENT_JSON_FOLDER / test_case_to.json_filename("S1000", i + 1)
        if os.path.exists(test_case_file_path):
            a = input(f"\x1b[95;49;5mthe file for \x1b[39;49mtest case {i + 1}\x1b[95;49;5m already exists. Press enter to skip or enter 'rerun' to remove it and rerun its test: \x1b[39;49m")
            if a.lower() != 'rerun':
                continue
            os.remove(test_case_file_path)
        tests_to_run.append(i + 1)

    #Runs all test cases using num_threads threads
    while len(tests_to_run) > 0:
        # start num_threads threads
        while len(threads) < num_threads:
            next_test = 0
            for test in tests_to_run:
                if test not in in_progress:
                    next_test = test
            # exit loop if there are no more tests to run
            if next_test == 0:
                time.sleep(3)
                break
            threads.append(threading.Thread(target=get_json_s1000, args=(next_test,), name=f"thread - case {next_test}"))
            in_progress.append(next_test)
            tests_to_run.remove(next_test)
            threads[-1].start()
            time.sleep(22)

        #join threads so none run rogue
        for thread in threads:
            # if thread is finished running
            if not thread.is_alive():
                # remove the thread from in_progress. Uses the name to get the test case
                in_progress.remove(int(thread.name[14:]))
                # remove the thread from threads to make space for a new one
                threads.remove(thread)

        # wait for any unfinished threads to be done running
    for thread in threads:
        thread.join()
    
    csv_results_path = constants.S1000_CURRENT_RESULTS_FILE
    protected_point_parameters = constants.S1000_POINT_PROTECTION_PARAM_FILE

    #compare protected point values for each test case
    for i in range(NUMBER_OF_TESTS):
        current_json_file = constants.S1000_CURRENT_JSON_FOLDER / test_case_to.json_filename("S1000", i + 1)
        compare_point_protected_values("S1000", protected_point_parameters, current_json_file)

    # gets the test case and the expected radius values for those test cases from the parameter file
    radius_dict_list = read_csv(constants.S1000_RADIUS_PARAMETER_FILE)

    # loops through each test case and adds the values from the json files to the radius dict for each test case
    # after this loop each dictionary in the dict list will have test case, expected r2 and r5, and actual r2 and r5
    for i in range(NUMBER_OF_TESTS):
        radius_dict_list[i].update(get_test_radius_results(constants.S1000_CURRENT_JSON_FOLDER / test_case_to.json_filename("S1000", i + 1)))

    # output radius results
    write_output_to_csv(csv_results_path, radius_dict_list)