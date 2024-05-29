from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from values_from_test_case import *

import time
from dotenv import load_dotenv
import os

load_dotenv()
AUTODESK_USERNAME = os.getenv('AUTODESK_USERNAME')
NVENT_USERNAME = os.getenv('NVENT_USERNAME')
NVENT_PASSWORD = os.getenv('NVENT_PASSWORD')

#Function to login to the qa website. Seems to differ from user to user.
def login():
    try:
        search_button = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "autodeskSigninButton")))
        search_button.click()
        time.sleep(1)

        input_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "userName")))
        input_field.send_keys(AUTODESK_USERNAME)
        
        submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "verify_user_btn")))
        submit_button.click()

        allow_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "allow_btn")))
        allow_button.click()
        time.sleep(5)
    except:
        print("failed to login")

def configure_webdriver(test_case):
    options = Options()
    try:
        prefs = {'download.prompt_for_download"': False, \
             'download.default_directory' : str(generate_folder_location("S1000 TEST",test_case))}

        options.add_experimental_option("prefs", prefs)
        #options.add_experimental_option("excludeSwitches", ["enable-logging"])
        global driver
        driver = webdriver.Edge(options=options)
    except:
        print("failed to start webdriver")

# Loads LPSD and pulls json output of input test case
def get_json(test_case):

    try:
        
        edit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//td[text() = '" +test_case_to_string("S1000", test_case)+"']/following-sibling::td/button")))
        edit_button.click()                                                      
        time.sleep(25)

        ActionChains(driver).key_down(Keys.ALT).key_down(Keys.CONTROL).send_keys("q").perform()
        time.sleep(1)
        ActionChains(driver).key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
        time.sleep(.2)

        debug_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "debugToolsButton")))
        debug_button.click()
        time.sleep(.2)

        debug_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "debugtools_exportanalysisresults_input")))
        debug_button.click()
        time.sleep(.2)

        debug_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "debugtools_exit_button")))
        debug_button.click()
        time.sleep(.2)

        debug_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "lpsd_toolbar_vertical_button_analysistools")))
        debug_button.click()
        time.sleep(.2)

        debug_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "lpsd_toolbar_vertical_button_analyze")))
        debug_button.click()
        time.sleep(1)

        checkbox_elements = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "analysis-startanalysis-step1-model")))
        checkbox_elements.click()
        time.sleep(1)

        next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "analysis_startanalysis_nextbutton1")))
        next_button.click()
        time.sleep(1)

        checkbox_elements = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "analysis-startanalysis-step3-method")))
        checkbox_elements.click()
        time.sleep(1)

        next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "analysis_startanalysis_nextbutton3")))
        next_button.click()
        time.sleep(1)

        next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "analysis_startanalysis_nextbutton4")))
        next_button.click()
        time.sleep(1)       

        next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "analysis_startanalysis_nextbutton5")))
        next_button.click()
        time.sleep(1)

        next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "analysis_analyzeproject_run_button")))
        next_button.click()
        time.sleep(7)

        next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "analysis_startanalysis_nextbutton6")))
        next_button.click()
        time.sleep(1)      

        next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "analysis_startanalysis_donebutton7")))
        next_button.click()
        time.sleep(1)

        print("JSON file successfully downloaded")

        driver.quit()
    except:
        print("Failed when acquiring JSON files.")


if __name__ == '__main__':
    global driver

    for i in [16]:#range(1,17,1):
        configure_webdriver(i)
        print(f"Beginning to run test case {i}")
        driver.get("https://qa-lpsd.nvent.com/")
        time.sleep(.5)
        login()
        get_json(i)

    driver.quit()