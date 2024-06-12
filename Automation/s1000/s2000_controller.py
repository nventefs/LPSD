import threading
from get_json import get_json_s2000
import test_case_to
from fileout import *
import constants

NUMBER_OF_TESTS = 4
NUMBER_OF_CASES = 8


if __name__ == '__main__':
    threads = []
    num_threads = int(input("How many threads would you like to use? (maximum 4 recommended): "))
    total_tests_done = 0
    cycle = 0

    #Runs all test cases using num_threads threads
    while True:
        for i in range(num_threads):
            threads.append(threading.Thread(target=get_json_s2000, args=(num_threads*cycle + i+1,), name=f"thread {i+1}"))
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

    for i in range (NUMBER_OF_CASES):
        if i % 2 == 0:
            compare_point_protected_values("S2000", constants.S2000_POINT_PROTECTION_PARAM_FILE_HALF_METER, constants.S2000_CURRENT_JSON_FOLDER / test_case_to.json_filename("S2000", i + 1))
        else:
            compare_point_protected_values("S2000", constants.S2000_POINT_PROTECTION_PARAM_FILE_ONE_METER, constants.S2000_CURRENT_JSON_FOLDER / test_case_to.json_filename("S2000", i + 1))


