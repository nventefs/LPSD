from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from tester_functions import *
import test_case_to as test_case_to
import threading
import time
from dotenv import load_dotenv
import os

load_dotenv()
AUTODESK_USERNAME = os.getenv('AUTODESK_USERNAME')
NVENT_USERNAME = os.getenv('NVENT_USERNAME')
NVENT_PASSWORD = os.getenv('NVENT_PASSWORD')

# fills in the options for the webdriver
def configure_webdriver(test_case):
    options = Options()

    #get path to test file
    file_path = test_case_to.file_path("S1000 TEST", test_case, generative=True, removing=True)
    
    # file was not found, return None, otherwise set default download directory to that file folder
    if file_path is not None:
        default_directory = str(file_path.parent)
    else:
        return None
    
    prefs = {'download.prompt_for_download"': False, 'download.default_directory' : default_directory}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--window-size=1920,1080")
    return options


# Loads LPSD and pulls json output of input test_case
def get_json(test_case):
    options = configure_webdriver(test_case)
    if options is None:
        print("Failed")
        return
    driver = webdriver.Edge(options=options)
    print(f"Beginning to run test case {test_case}")
    driver.get("https://qa-lpsd.nvent.com/")
    time.sleep(.5)
    login(driver, AUTODESK_USERNAME)

    time.sleep(5)

    try:
        click_element(driver, (By.XPATH, "//td[text() = '" + test_case_to.name("S1000", test_case)+"']/following-sibling::td/button"))
        time.sleep(35)

        ActionChains(driver).key_down(Keys.ALT).key_down(Keys.CONTROL).send_keys("q").perform()
        time.sleep(1)
        ActionChains(driver).key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
        time.sleep(1)

        click_element(driver,(By.ID, "debugToolsButton"))
        time.sleep(1)

        click_element(driver, (By.ID, "debugtools_exportanalysisresults_input"))
        time.sleep(1)

        click_element(driver, (By.ID, "debugtools_exit_button"))
        time.sleep(1)

        click_element(driver, (By.ID, "lpsd_toolbar_vertical_button_analysistools"))
        time.sleep(1)

        click_element(driver, (By.ID, "lpsd_toolbar_vertical_button_analyze"))
        time.sleep(1)

        click_element(driver, (By.CLASS_NAME, "analysis-startanalysis-step1-model"))
        time.sleep(1)

        click_element(driver, (By.ID, "analysis_startanalysis_nextbutton1"))
        time.sleep(1)

        click_element(driver, (By.CLASS_NAME, "analysis-startanalysis-step3-method"))
        time.sleep(1)

        click_element(driver, (By.ID, "analysis_startanalysis_nextbutton3"))
        time.sleep(1)

        click_element(driver, (By.ID, "analysis_startanalysis_nextbutton4"))
        time.sleep(1)       

        click_element(driver, (By.ID, "analysis_startanalysis_nextbutton5"))
        time.sleep(1)

        click_element(driver, (By.ID, "analysis_analyzeproject_run_button"))
        time.sleep(9)

        click_element(driver, (By.ID, "analysis_startanalysis_nextbutton6"))
        time.sleep(1)

        click_element(driver, (By.ID, "analysis_startanalysis_donebutton7"))
        time.sleep(1)
        print("JSON file successfully downloaded")
    except:
        print("Failed when acquiring JSON files.")
    print (f"{threading.current_thread().name} finished running test case {test_case}")
    driver.quit()


# loop through the 16 cases and pull their json files
if __name__ == '__main__':
    start_time = time.time()
    threads = []
    for cycle in range(4):
        for i in range(4):
            threads.append(threading.Thread(target=get_json, args=(4*cycle + i+1,), name=f"thread {i+1}"))
            threads[i].start()
        for _ in range(4):
            threads[0].join()
            threads.pop(0)
    
    end_time = time.time()
    print (f"Total time to run program: {end_time - start_time}")
