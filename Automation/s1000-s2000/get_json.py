from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from tester_functions import *
import test_case_to
import threading
import time
import os
import constants

START_LINK = "https://qa-lpsd.nvent.com/"

# a simple decorator that will retry a function 20 times with a one second break until it returns true
def repeat_until_successful(func):
    def wrapper(*args, **kwargs):
        for _ in range(20):
            if func(*args, **kwargs):
                return True
            time.sleep(1)
        else:
            return False
    return wrapper

#Starts the test, just a function to click the button with a decorator
@repeat_until_successful
def start_test (driver, type, test_case):
    return click_element(driver, (By.XPATH, "//td[text() = '" + test_case_to.name(type, test_case)+"']/following-sibling::td/button"))

# presses ctrl + alt + q and clicks export analysis then exits
@repeat_until_successful
def turn_on_export_analysis(driver:webdriver.Edge):
    # press ctrl+alt+q
    ActionChains(driver).key_down(Keys.ALT).key_down(Keys.CONTROL).send_keys("q").perform()
    time.sleep(1)
    ActionChains(driver).key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
    time.sleep(1)

    # clicks the debug tools button to open menu
    if not click_element(driver,(By.ID, "debugToolsButton")):
        return False
    time.sleep(1)

    # only if the checkbox is not already selected, it will get clicked
    try:
        checkbox = driver.find_element(By.ID, "debugtools_exportanalysisresults_input")
        if not checkbox.is_selected():
            if not click_element(driver, (By.ID, "debugtools_exportanalysisresults_input")):
                return False
    except:
        return False

    time.sleep(1)

    # close debug tools menu
    if not click_element(driver, (By.ID, "debugtools_exit_button")):
        return False
    time.sleep(1)
    return True

#clicks through all the buttons to get the json file. These are the same for every test case.
@repeat_until_successful
def click_through_analysis(driver):
    if not click_element(driver, (By.ID, "lpsd_toolbar_vertical_button_analysistools")):
        return False
    time.sleep(1)

    if not click_element(driver, (By.ID, "lpsd_toolbar_vertical_button_analyze")):
        return False
    time.sleep(1)

    if not click_element(driver, (By.CLASS_NAME, "analysis-startanalysis-step1-model")):
        return False
    time.sleep(1)

    if not click_element(driver, (By.ID, "analysis_startanalysis_nextbutton1")):
        return False
    time.sleep(1)

    if not click_element(driver, (By.CLASS_NAME, "analysis-startanalysis-step3-method")):
        return False
    time.sleep(1)

    if not click_element(driver, (By.ID, "analysis_startanalysis_nextbutton3")):
        return False
    time.sleep(1)

    if not click_element(driver, (By.ID, "analysis_startanalysis_nextbutton4")):
        return False
    time.sleep(1)       

    if not click_element(driver, (By.ID, "analysis_startanalysis_nextbutton5")):
        return False
    time.sleep(1)

    if not click_element(driver, (By.ID, "analysis_analyzeproject_run_button")):
        return False
    time.sleep(15)

    if not click_element(driver, (By.ID, "analysis_startanalysis_nextbutton6")):
        return False
    time.sleep(1)

    if not click_element(driver, (By.ID, "analysis_startanalysis_donebutton7")):
        return False
    time.sleep(1)
    return True

# pulls json output for the type and test case
def get_json(driver: webdriver.Edge, type, test_case):
    print(f"Beginning to run test case {test_case}")
    # goes to the original link if the driver has already run a test
    driver.get(START_LINK)
    time.sleep(.5)
    # clicks okay on the warning box that says "your changes might not be saved"
    try:
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(1)
    except:
        pass

    # click on button to open the test
    if not start_test(driver, type, test_case):
        return None
    
    # select option to export analysis
    if not turn_on_export_analysis(driver):
        return None
    
    # if type is S2000 choose half or one meter points based on if its an odd or even test case
    if type == "S2000":
        time.sleep(1)
        if test_case % 2 == 1:
            choose_combobox_value(driver, (By.ID, "dashboard_project_option_select"), choice="manual", manual_values=["HALF METER POINTS"])
        else:
            choose_combobox_value(driver, (By.ID, "dashboard_project_option_select"), choice="manual", manual_values=["ONE METER POINTS"])

    # click through all the buttons required to run the analysis and download the json file
    if not click_through_analysis(driver):
        return None
    
    # rename the file for S2000 because case 1 and 2, 3 and 4, etc have the same name since their only difference is changing the combobox value above
    if type == "S2000":
        json_folder = constants.S2000_CURRENT_JSON_FOLDER
        old_file_path = json_folder / (test_case_to.name("S2000", test_case) + "_RSResults.json")
        new_file_path = json_folder / test_case_to.json_filename("S2000", test_case)
        os.rename(old_file_path, new_file_path)

    # tell user that the file for the current test case should be done
    print (f"finished running test case {test_case}. {test_case_to.json_filename(type,test_case)} should have downloaded.")
