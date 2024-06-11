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
def configure_webdriver(type, test_case):
    options = Options()

    #get path to test file
    folder_path = test_case_to.folder_path(type, generative=True)
    
    default_directory = str(folder_path)
    
    prefs = {'download.prompt_for_download"': False, 'download.default_directory' : default_directory}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--window-size=1920,1080")
    return options

def turn_on_export_analysis(driver):
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

#clicks through all the buttons to get the json file. These are the same for every test case.
def click_through_analysis(driver):
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
    time.sleep(15)

    if not click_element(driver, (By.ID, "analysis_startanalysis_nextbutton6")):
        return None
    time.sleep(1)

    if not click_element(driver, (By.ID, "analysis_startanalysis_donebutton7")):
        return None
    time.sleep(1)

# Loads LPSD and pulls json output of input test_case
def get_json_s1000(test_case):
    print(f"configuring test case {test_case}")
    options = configure_webdriver("S1000 TEST", test_case)
    if options is None:
        print(f"Skipping Test Case {test_case}")
        return
    
    file_path = test_case_to.file_path(type, test_case, generative=False, removing=False)
    if file_path is not None:
        a = input("\x1b[95;49;5mThis file already exists. Press enter to skip or enter 'rerun' to remove it and rerun its test: \x1b[39;49m")
        if a.lower() != 'rerun':
            return
        file_path = test_case_to.file_path(type, test_case, generative=True, removing=True)

    driver = webdriver.Edge(options=options)
    print(f"Beginning to run test case {test_case}")
    driver.get("https://qa-lpsd.nvent.com/")
    time.sleep(.5)
    login(driver, AUTODESK_USERNAME)
    time.sleep(10)
    if not click_element(driver, (By.XPATH, "//td[text() = '" + test_case_to.name("S1000", test_case)+"']/following-sibling::td/button")):
        return None
    time.sleep(40)
    turn_on_export_analysis(driver)
    click_through_analysis(driver)
    print (f"{threading.current_thread().name} finished running test case {test_case}. {test_case_to.json_filename("S1000 Test",test_case)} successfully downloaded.")
    driver.quit()

def get_json_s2000(test_case):

    print(f"configuring test case {test_case}")
    options = configure_webdriver("S2000 TEST", test_case)
    driver = webdriver.Edge(options=options)
    print(f"Beginning to run test case {test_case}")
    driver.get("https://qa-lpsd.nvent.com/")
    time.sleep(.5)
    login(driver, AUTODESK_USERNAME)
    time.sleep(10)
    if not click_element(driver, (By.XPATH, "//td[text() = '" + test_case_to.name("S2000", test_case)+"']/following-sibling::td/button")):
        return None
    time.sleep(40)

    turn_on_export_analysis(driver)
    choose_combobox_value(driver, (By.ID, "dashboard_project_option_select"), choice="manual", manual_values=["HALF METER POINTS"])
    click_through_analysis(driver)

    folder_path = test_case_to.folder_path("S2000 TEST")
    old_file_path = folder_path / test_case_to.json_filename("S2000 OLD", test_case)
    new_file_path = folder_path / test_case_to.json_filename("S2000 HALF", test_case)

    os.rename(old_file_path, new_file_path)
    choose_combobox_value(driver, (By.ID, "dashboard_project_option_select"), choice="manual", manual_values=["ONE METER POINTS"])
    click_through_analysis(driver)

    new_file_path = folder_path / test_case_to.json_filename("S2000 ONE", test_case)
    os.rename(old_file_path, new_file_path)

    print (f"{threading.current_thread().name} finished running test case {test_case}. {test_case_to.json_filename("S1000 Test",test_case)} successfully downloaded.")
    driver.quit()