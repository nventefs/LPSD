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

def close_tab(driver):
    ActionChains(driver).key_down(Keys.CONTROL).send_keys("w").perform()
    time.sleep(1)
    ActionChains(driver).key_up(Keys.CONTROL).perform()
    time.sleep(1)

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
def get_json_s1000(driver: webdriver.Edge, test_case):
    print(f"Beginning to run test case {test_case}")
    
   # driver.execute_script("window.open('about:blank', '_blank');")
    #time.sleep(1)
    # Switch to the new tab
    #driver.switch_to.window(driver.window_handles[-1])

    driver.get(START_LINK)
    time.sleep(.5)
    try:
        alert = driver.switch_to.alert
        # If an alert is present, print its text and accept it
        alert.accept()  # Accept the alert (click OK)
        time.sleep(1)
    except:
        pass
    while not click_element(driver, (By.XPATH, "//td[text() = '" + test_case_to.name("S1000", test_case)+"']/following-sibling::td/button")):
        #try until the button is ready to be clicked
        time.sleep(2)
    time.sleep(40)
    turn_on_export_analysis(driver)
    click_through_analysis(driver)
    print("Clicking")
    ActionChains(driver).click()
    print("Clicked")
    print (f"{threading.current_thread().name} finished running test case {test_case}. {test_case_to.json_filename("S1000",test_case)} successfully downloaded.")

def get_json_s2000(driver, test_case):
    print(f"Beginning to run test case {test_case}")
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