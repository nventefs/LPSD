import threading
from get_json import get_json_s2000
import test_case_to
from fileout import *

NUMBER_OF_TESTS = 4



if __name__ == '__main__':
    threads = []
    num_threads = int(input("How many threads would you like to use? (maximum 4 recommended): "))
    total_tests_done = 3
    cycle = 3

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
