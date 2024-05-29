from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import time
from dotenv import load_dotenv
import os
import datetime
from pathlib import Path

load_dotenv()
AUTODESK_USERNAME = os.getenv('AUTODESK_USERNAME')
NVENT_USERNAME = os.getenv('NVENT_USERNAME')
NVENT_PASSWORD = os.getenv('NVENT_PASSWORD')

# Sanitizes yes/no input from terminal
def sanitize_input(input_str):
    return input_str.lower()


# Generates a folder location of Archive\JSON\yyyy-mm-dd
def generate_folder_location(test_case):

    # Generate a folder within archive/s1000/json for the current test case
    root_dir = Path(__file__).resolve().parent.parent
    folder_location = root_dir / "Archive" / "s1000" / "JSON"
    folder_name = datetime.datetime.now().strftime("%Y-%m-%d")

    directory_name = str(folder_location) + "\\" + folder_name
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
        print(f"Directory '{directory_name}' created successfully.")
        return(directory_name)
    else:
        print(f"Directory '{directory_name}' already exists")
        if os.path.isfile(directory_name + test_case_to_json(test_case, "S1000")):
            print(directory_name + test_case_to_json(test_case, "S1000") + "  exists!")
            x = input("Continue with JSON fetch? ")
            try: 
                if(sanitize_input(x) == "no"):
                    return
                else:
                    return(directory_name)
            except:
                print("Input not recognized.")
        else:
            return(directory_name)

# Selector for .json file names
# TODO: Change pathing to reference pathing for scaleability
def test_case_to_json(test_case, type):
    cvm_tc = {
        1: "CVM Test Case 1 metric_CVMResults.json",
        2: "CVM Test Case 2_CVMResults.json",
        3: "CVM Test Case 3 Rev B_CVMResults.json",
        4: "CVM Test Case 4_CVMResults.json",
        5: "CVM Test Case 5_CVMResults.json",
        6: "CVM Test Case 6 Rev F_CVMResults.json",
        7: "CVM Test Case 7_CVMResults.json",
    }

    s1000_tc = {
        1: "S1000 QA TC1.json",
        2: "S1000 QA TC2.json",
        3: "S1000 QA TC3.json",
        4: "S1000 QA TC4.json",
        5: "S1000 QA TC5.json",
        6: "S1000 QA TC6.json",
        7: "S1000 QA TC7.json",
        8: "S1000 QA TC8.json",
        9: "S1000 QA TC9.json",
        10: "S1000 QA TC10.json",
        11: "S1000 QA TC11.json",
        12: "S1000 QA TC12.json",
        13: "S1000 QA TC13.json",
        14: "S1000 QA TC14.json",
        15: "S1000 QA TC15.json",
        16: "S1000 QA TC16.json",
    }

    match (type):
        case "CVM":
            return cvm_tc.get(test_case)
        case "S1000":
            return s1000_tc.get(test_case)

# Selector for test case name
# TODO: Change pathing to reference pathing for scaleability
def test_case_to_string(test_case, type):
    cvm_tc = {
        1: "CVM Test Case 1 metric",
        2: "CVM Test Case 2",
        3: "CVM Test Case 3 Rev B",
        4: "CVM Test Case 4",
        5: "CVM Test Case 5",
        6: "CVM Test Case 6 Rev F",
        7: "CVM Test Case 7"
    }

    s1000_tc = {
        1: "S1000 QA TC1",
        2: "S1000 QA TC2",
        3: "S1000 QA TC3",
        4: "S1000 QA TC4",
        5: "S1000 QA TC5",
        6: "S1000 QA TC6",
        7: "S1000 QA TC7",
        8: "S1000 QA TC8",
        9: "S1000 QA TC9",
        10: "S1000 QA TC10",
        11: "S1000 QA TC11",
        12: "S1000 QA TC12",
        13: "S1000 QA TC13",
        14: "S1000 QA TC14",
        15: "S1000 QA TC15",
        16: "S1000 QA TC16",
    }

    match (type):
        case "CVM":
            return cvm_tc.get(test_case)
        case "S1000":
            return s1000_tc.get(test_case)

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
             'download.default_directory' : generate_folder_location(test_case)}
        options.add_experimental_option("prefs", prefs)
        #options.add_experimental_option("excludeSwitches", ["enable-logging"])
        global driver
        driver = webdriver.Edge(options=options)
    except:
        print("failed to start webdriver")

# Loads LPSD and pulls json output of input test case
def get_json(test_case):

    try:
        
        edit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//td[text() = '" +test_case_to_string(test_case, "S1000")+"']/following-sibling::td/button")))
        edit_button.click()                                                      
        time.sleep(35)

        ActionChains(driver).key_down(Keys.ALT).key_down(Keys.CONTROL).send_keys("q").perform()
        time.sleep(1)
        ActionChains(driver).key_up(Keys.ALT).key_up(Keys.CONTROL).perform()

        debug_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "debugToolsButton")))
        debug_button.click()
        time.sleep(3)

        debug_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "debugtools_exportanalysisresults_input")))
        debug_button.click()
        time.sleep(1)

        debug_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "debugtools_exit_button")))
        debug_button.click()
        time.sleep(1)

        debug_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "lpsd_toolbar_vertical_button_analysistools")))
        debug_button.click()
        time.sleep(1)

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
        time.sleep(12)

        next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "analysis_startanalysis_nextbutton6")))
        next_button.click()
        time.sleep(1)       

        next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "analysis_startanalysis_donebutton7")))
        next_button.click()
        time.sleep(1)

        print("end")
        time.sleep(10)

        driver.quit()
    except:
        print("Failed when acquiring JSON files.")


if __name__ == '__main__':
    global driver

    for i in range(1,17,1):
        configure_webdriver(i)
        print(f"Beginning to run test case {i}")
        driver.get("https://qa-lpsd.nvent.com/")
        time.sleep(5)
        login()
        get_json(i)


    driver.quit()