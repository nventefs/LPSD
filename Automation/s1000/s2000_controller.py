import threading
from get_json import get_json_s2000
import test_case_to
from fileout import *
import constants
import os
import time

# there are two cases per test: half meter and one meter
NUMBER_OF_TESTS = 8


if __name__ == '__main__':
    threads = []
    tests_to_run = []
    in_progress = []
    num_threads = int(input("How many threads would you like to use? (maximum 4 recommended): "))

    for i in range (NUMBER_OF_TESTS):
        test_case_file_path = constants.S2000_CURRENT_JSON_FOLDER / test_case_to.json_filename("S2000", i + 1)
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
                    if test % 2 == 0:
                        if test - 1 not in in_progress:
                            next_test = test
                    else:
                        if test + 1 not in in_progress:
                            next_test = test
            # exit loop if there are no more tests to run
            if next_test == 0:
                time.sleep(3)
                break
            threads.append(threading.Thread(target=get_json_s2000, args=(next_test,), name=f"thread - case {next_test}"))
            in_progress.append(next_test)
            tests_to_run.remove(next_test)
            threads[-1].start()
            time.sleep(25)

        #join threads so none run rogue
        for thread in threads:
            # if thread is finished running
            if not thread.is_alive():
                # remove the thread from in_progress. Uses the name to get the test case
                in_progress.remove(int(thread.name[-1]))
                # remove the thread from threads to make space for a new one
                threads.remove(thread)

    # wait for any unfinished threads to be done running
    for thread in threads:
        thread.join()

    # compare protected point values for each test case
    for i in range (NUMBER_OF_TESTS):
        current_json_file = constants.S2000_CURRENT_JSON_FOLDER / test_case_to.json_filename("S2000", i + 1)
        # since the same test has the half meter and full meter version both cases for the same test have the same point guids, but different protected point values
        # odd test cases (half meter) use one file, while even test cases use another
        # even though i % 2 == 0, it is used for half meter cases because we add 1 when calling test_case_to.json_filename 
        if i % 2 == 0:
            compare_point_protected_values("S2000", constants.S2000_POINT_PROTECTION_PARAM_FILE_HALF_METER, current_json_file)
        else:
            compare_point_protected_values("S2000", constants.S2000_POINT_PROTECTION_PARAM_FILE_ONE_METER, current_json_file)


