import threading
import os
from get_json import get_json
import test_case_to
from fileout import *

NUMBER_OF_TESTS = 16

if __name__ == '__main__':
    threads = []
    num_threads = int(input("How many threads would you like to use? (maximum 4 recommended): "))
    total_tests_done = 15
    cycle = 12


    #Runs all 16 test cases using num_threads threads
    while True:
        for i in range(num_threads):
            threads.append(threading.Thread(target=get_json, args=(num_threads*cycle + i+1,), name=f"thread {i+1}"))
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

    
    dict_list = []
    radii_csv_path = test_case_to.file_path("S1000 OUTPUT", generative=True, removing=True)
    json_filepath = test_case_to.file_path("S1000 PROTECTEDPOINTS",generative=True,removing=False)
    protected_values_dict = {}

    for i in range(NUMBER_OF_TESTS):
        protected_values_dict.update(get_point_protected_values(i+1))
    #write_json(protected_values_dict, json_filepath)
    for i in range(NUMBER_OF_TESTS):
        compare_point_protected_values(i+1)


    for i in range(NUMBER_OF_TESTS):
        dict_list.append(get_radii_dict(i + 1))
    write_output_to_csv(radii_csv_path, dict_list)