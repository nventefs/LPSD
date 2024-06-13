from custom_driver import LPSDDriver
from get_json import get_json_s1000
import test_case_to
from fileout import *
import constants
import os
import signal
import sys
import time
from typing import List
from killable_thread import KillableThread

NUMBER_OF_TESTS = 16
drivers: List[LPSDDriver] = []

# function to create a new webdriver
# can only create one every 30 seconds because of two factor authentication limits
def start_drivers(number_of_drivers):
    while len(drivers) < number_of_drivers:
        drivers.append(LPSDDriver(type="S1000"))
        time.sleep(30)

# returns a driver that is not currently running a test or returns none if there are no such drivers
def get_inactive_driver():
    for driver in drivers:
        if not driver.active:
            return driver
    time.sleep(3)
    return None

def set_driver_inactive(associated_test):
    for driver in drivers:
        if driver.associated_test == associated_test:
            driver.active = False

def signal_handler(signal, frame):
    print("You ended the program. Killing all threads.")
    for thread in threads:
        thread.kill()
    start_drivers_thread.kill()
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    threads: List[KillableThread] = []
    tests_to_run = []
    in_progress = []
    num_threads = int(input("How many threads would you like to use? (maximum 4 recommended): "))

    # create a thread that will start the correct number of drivers and only start one every 30 seconds to avoid 2 factor authentication issues
    start_drivers_thread = KillableThread(target=start_drivers, args=(num_threads,),name="Driver start thread")
    start_drivers_thread.start()

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
            # exit loop if there are no more tests to run, wait a few seconds to avoid constantly running cpu
            if next_test == 0:
                time.sleep(3)
                break
            # add a thread that calls the test case for next_test for the thread
            inactive_driver = get_inactive_driver()
            # if we found an inactive driver
            if inactive_driver is not None:
                # set its associated test to the test it will run
                inactive_driver.associated_test = next_test
                # set it to active so it wont be used by another test
                inactive_driver.active = True
                # create a thread that will run the test case
                threads.append(KillableThread(target=get_json_s1000, args=(inactive_driver, next_test), name=f"{next_test}"))
                # set the test case to in progress so no other threads run it
                in_progress.append(next_test)
                # start the most recent thread added to the list
                threads[-1].start()

        for thread in threads:
            # if thread is finished running
            if not thread.is_alive():
                test_case = int(thread.name)
                # remove the thread from in_progress. Uses the name to get the test case
                in_progress.remove(test_case)
                # remove the thread from threads to make space for a new one
                threads.remove(thread)
                set_driver_inactive(test_case)
                # test if the file actually downloaded, if it did, take it out of the list of tests that arent done
                test_case_file_path = constants.S1000_CURRENT_JSON_FOLDER / test_case_to.json_filename("S1000", test_case)
                if os.path.exists(test_case_file_path):
                    tests_to_run.remove(test_case)
    
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

    #kill all threads that are still running in case there are any somehow
    for thread in threads:
        thread.kill()
    start_drivers_thread.kill()
