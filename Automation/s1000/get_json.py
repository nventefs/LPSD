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
import constants

load_dotenv()
AUTODESK_USERNAME = os.getenv('AUTODESK_USERNAME')
NVENT_USERNAME = os.getenv('NVENT_USERNAME')
NVENT_PASSWORD = os.getenv('NVENT_PASSWORD')
TWO_FACTOR_KEY = os.getenv('TWO_FACTOR_KEY')

# fills in the options for the webdriver
# sets default window size and download folder
def configure_webdriver(type):
    options = Options()

    #get path to test file
    if type == "S1000":
        folder_path = constants.S1000_CURRENT_JSON_FOLDER
    elif type == "S2000":
        folder_path = constants.S2000_CURRENT_JSON_FOLDER

    # make the folder if it doesnt exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # set folder for driver to download to the folder we just made
    default_directory = str(folder_path)
    
    # set some options
    prefs = {'download.prompt_for_download"': False, 'download.default_directory' : default_directory}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--window-size=1920,1080")

    return options

# presses ctrl + alt + q and clicks export analysis then exits
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

# pulls json output for the s1000 test case
def get_json_s1000(test_case):
    print(f"configuring test case {test_case}")
    options = configure_webdriver("S1000")

    driver = webdriver.Edge(options=options)
    print(f"Beginning to run test case {test_case}")
    driver.get("https://qa-lpsd.nvent.com/")
    time.sleep(.5)
    login(driver, AUTODESK_USERNAME, TWO_FACTOR_KEY)
    time.sleep(10)
    if not click_element(driver, (By.XPATH, "//td[text() = '" + test_case_to.name("S1000", test_case)+"']/following-sibling::td/button")):
        return None
    time.sleep(40)
    turn_on_export_analysis(driver)
    click_through_analysis(driver)
    print (f"{threading.current_thread().name} finished running test case {test_case}. {test_case_to.json_filename("S1000",test_case)} successfully downloaded.")
    driver.quit()

def get_json_s2000(test_case):
    print(f"configuring test case {test_case}")
    options = configure_webdriver("S2000")

    driver = webdriver.Edge(options=options)
    print(f"Beginning to run test case {test_case}")
    driver.get("https://qa-lpsd.nvent.com/")
    time.sleep(.5)
    login(driver, AUTODESK_USERNAME, TWO_FACTOR_KEY)
    time.sleep(10)
    if not click_element(driver, (By.XPATH, "//td[text() = '" + test_case_to.name("S2000", test_case)+"']/following-sibling::td/button")):
        return None
    time.sleep(40)

    turn_on_export_analysis(driver)
    if test_case % 2 == 1:
        choose_combobox_value(driver, (By.ID, "dashboard_project_option_select"), choice="manual", manual_values=["HALF METER POINTS"])
    else:
        choose_combobox_value(driver, (By.ID, "dashboard_project_option_select"), choice="manual", manual_values=["ONE METER POINTS"])
    click_through_analysis(driver)

    json_folder = constants.S2000_CURRENT_JSON_FOLDER
    old_file_path = json_folder / (test_case_to.name("S2000", test_case) + "_RSResults.json")
    new_file_path = json_folder / test_case_to.json_filename("S2000", test_case)
    os.rename(old_file_path, new_file_path)

    print (f"{threading.current_thread().name} finished running test case {test_case}. {test_case_to.json_filename("S2000",test_case)} successfully downloaded.")
    driver.quit()