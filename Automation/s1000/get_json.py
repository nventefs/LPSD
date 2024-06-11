from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from tester_functions import *
import test_case_to
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
    test_case_to.folder_path("S1000 TEST", generative=True)
    file_path = test_case_to.file_path("S1000 TEST", test_case, generative=False, removing=False)
    if file_path is not None:
        a = input("\x1b[95;49;5mThis file already exists. Press enter to skip or enter 'rerun' to remove it and rerun its test: \x1b[39;49m")
        if a.lower() != 'rerun':
            return None
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
    print(f"configuring test case {test_case}")
    options = configure_webdriver(test_case)
    if options is None:
        print(f"Skipping Test Case {test_case}")
        return
    driver = webdriver.Edge(options=options)
    print(f"Beginning to run test case {test_case}")
    driver.get("https://qa-lpsd.nvent.com/")
    time.sleep(.5)
    login(driver, AUTODESK_USERNAME)

    time.sleep(10)

    if not click_element(driver, (By.XPATH, "//td[text() = '" + test_case_to.name("S1000", test_case)+"']/following-sibling::td/button")):
        return None
    time.sleep(40)

    ActionChains(driver).key_down(Keys.ALT).key_down(Keys.CONTROL).send_keys("q").perform()
    time.sleep(1)
    ActionChains(driver).key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
    time.sleep(1)

    if not click_element(driver,(By.ID, "debugToolsButton")):
        return None
    time.sleep(1)

    if not click_element(driver, (By.ID, "debugtools_exportanalysisresults_input")):
        return None
    time.sleep(1)

    if not click_element(driver, (By.ID, "debugtools_exit_button")):
        return None
    time.sleep(1)

    if not click_element(driver, (By.ID, "lpsd_toolbar_vertical_button_analysistools")):
        return None
    time.sleep(1)

    if not click_element(driver, (By.ID, "lpsd_toolbar_vertical_button_analyze")):
        return None
    time.sleep(1)

    if not click_element(driver, (By.CLASS_NAME, "analysis-startanalysis-step1-model")):
        return None
    time.sleep(1)

    if not click_element(driver, (By.ID, "analysis_startanalysis_nextbutton1")):
        return None
    time.sleep(1)

    if not click_element(driver, (By.CLASS_NAME, "analysis-startanalysis-step3-method")):
        return None
    time.sleep(1)

    if not click_element(driver, (By.ID, "analysis_startanalysis_nextbutton3")):
        return None
    time.sleep(1)

    if not click_element(driver, (By.ID, "analysis_startanalysis_nextbutton4")):
        return None
    time.sleep(1)       

    if not click_element(driver, (By.ID, "analysis_startanalysis_nextbutton5")):
        return None
    time.sleep(1)

    if not click_element(driver, (By.ID, "analysis_analyzeproject_run_button")):
        return None
    time.sleep(9)

    if not click_element(driver, (By.ID, "analysis_startanalysis_nextbutton6")):
        return None
    time.sleep(1)

    if not click_element(driver, (By.ID, "analysis_startanalysis_donebutton7")):
        return None
    time.sleep(1)
    
    print (f"{threading.current_thread().name} finished running test case {test_case}. {test_case_to.json_filename("S1000 Test",test_case)} successfully downloaded.")
    driver.quit()
