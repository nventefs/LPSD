"""
    This file controls the testing functions to get the json files and output results for LPSD system 1000 and system 2000
    I used a multithreaded approach to accomplish this. Originally, I used one driver and one thread every time I created a test case
    but I learned that 2 factor authentication does not allow you to sign into multiple things at the same time for a single account, 
    so you must wait around 30 seconds between logins to be safe. This meant that the maximum rate that I could reliably start a 
    webdriver, and thus a test case, was once every 30 seconds. This works but is rather slow and was also inconsistent because logins would start to overlap.
    To solve this, I made a little driver subclass that could tell if it was actively running a test and which test it was running.
    This way, I could asynchronously start the drivers and just keep a list of them, then every once in a while, the program checks to see if any are inactive.
    If a driver is inactive, it is assigned a test case that is not "in progress", and it runs it. After all the files are downloaded,
    the results are compared as they should be and the drivers and threads are killed off.
"""

from custom_driver import LPSDDriver
from get_json import get_json
import test_case_to
from fileout import *
import constants
import os
import signal
import sys
import time
from typing import List
from killable_thread import KillableThread

NUMBER_OF_TESTS_S1000 = 16
NUMBER_OF_TESTS_S2000 = 16
drivers: List[LPSDDriver] = []
threads: List[KillableThread] = []

# function to create a new webdriver
# can only create one every 30 seconds because of two factor authentication limits
def start_drivers(number_of_drivers, type):
    while len(drivers) < number_of_drivers:
        driver = LPSDDriver(type=type)
        drivers.append(driver)
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

def kill_threads():
    #kill all threads that are still running in case there are any somehow
    for thread in threads:
        thread.kill()
    start_drivers_thread.kill()

def signal_handler(signal, frame):
    print("You ended the program. Attempting to kill all threads.")
    kill_threads()
    sys.exit(0)

def run_controller(type, num_threads):
    global start_drivers_thread
    global number_of_tests
    signal.signal(signal.SIGINT, signal_handler)

    tests_to_run = []
    in_progress = []
    if type == "S1000":
        number_of_tests = NUMBER_OF_TESTS_S1000 
    elif type == "S2000":
        number_of_tests = NUMBER_OF_TESTS_S2000
    # create a thread that will start the correct number of drivers and only start one every 30 seconds to avoid 2 factor authentication issues
    start_drivers_thread = KillableThread(target=start_drivers, args=(num_threads,type),name="Driver start thread")
    start_drivers_thread.start()

    for i in range (number_of_tests):
        if type == "S1000":
            test_case_file_path = constants.S1000_CURRENT_JSON_FOLDER / test_case_to.json_filename(type, i + 1)
        elif type == "S2000":
            test_case_file_path = constants.S2000_CURRENT_JSON_FOLDER / test_case_to.json_filename(type, i + 1)
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
                    if type == "S1000":
                        next_test = test
                    elif type == "S2000":
                        if test % 2 == 0:
                            if test - 1 not in in_progress:
                                next_test = test
                        else:
                            if test + 1 not in in_progress:
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
                threads.append(KillableThread(target=get_json, args=(inactive_driver, type, next_test), name=f"{next_test}"))
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
                if type == "S1000":
                    test_case_file_path = constants.S1000_CURRENT_JSON_FOLDER / test_case_to.json_filename(type, test_case)
                elif type == "S2000":
                    test_case_file_path = constants.S2000_CURRENT_JSON_FOLDER / test_case_to.json_filename(type, test_case)
                if os.path.exists(test_case_file_path):
                    tests_to_run.remove(test_case)
    

def check_protected_points(type):
    if type == "S1000":
        protected_point_parameters = constants.S1000_POINT_PROTECTION_PARAM_FILE
        
    #compare protected point values for each test case
    for i in range(number_of_tests):
        if type == "S1000":
            current_json_file = constants.S1000_CURRENT_JSON_FOLDER / test_case_to.json_filename(type, i + 1)
            compare_point_protected_values(type, protected_point_parameters, current_json_file)
        elif type == "S2000":
            current_json_file = constants.S2000_CURRENT_JSON_FOLDER / test_case_to.json_filename(type, i + 1)
            if i % 2 == 0:
                protected_point_parameters = constants.S2000_POINT_PROTECTION_PARAM_FILE_HALF_METER
                compare_point_protected_values(type, protected_point_parameters, current_json_file)
            else:
                protected_point_parameters = constants.S2000_POINT_PROTECTION_PARAM_FILE_ONE_METER
                compare_point_protected_values(type, protected_point_parameters, current_json_file)
                


def get_radii_csv():
    # gets the test case and the expected radius values for those test cases from the parameter file
    radius_dict_list = read_csv(constants.S1000_RADIUS_PARAMETER_FILE)
    csv_results_path = constants.S1000_CURRENT_RESULTS_FILE

    # loops through each test case and adds the values from the json files to the radius dict for each test case
    # after this loop each dictionary in the dict list will have test case, expected r2 and r5, and actual r2 and r5
    for i in range(number_of_tests):
        radius_dict_list[i].update(get_test_radius_results(constants.S1000_CURRENT_JSON_FOLDER / test_case_to.json_filename("S1000", i + 1)))

    # output radius results
    write_output_to_csv(csv_results_path, radius_dict_list)

if __name__ == '__main__':
    
    type = input("What tests would you like to run? (S1000/S2000): ")
    num_threads = int(input("How many threads would you like to use? (Maximum of 4 recommended): "))
    run_controller(type, num_threads)
    check_protected_points(type)
    if type == "S1000":
        get_radii_csv()
    kill_threads()