from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import datetime
import os

# Sanitizes yes/no input from terminal
def sanitize_input(input_str):
    if input_str == "Yes" or input_str == "YES" or input_str == "yEs" or input_str == "yes":
        return "yes"
    elif input_str == "No" or input_str == "NO" or input_str == "no":
        return "no"
    else:
        raise

# Generates a folder location of Archive\JSON\yyyy-mm-dd
def generate_folder_location(test_case):

    # Generate a folder C:\Users\e1176752\Documents\VSCode\Projects\LPSD\LPSD
    folder_location = "C:/Users/e1176752/Documents/VSCode/Projects/LPSD/LPSD/Archive/JSON/"
    folder_name = datetime.datetime.now().strftime("%Y-%m-%d")

    directory_name = folder_location + folder_name
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
        print(f"Directory '{directory_name}' created successfully.")
    else:
        print(f"Directory '{directory_name}' already exists")
        if os.path.isfile(directory_name + test_case_to_json(test_case)):
            print(directory_name + test_case_to_json(test_case) + "  exists!")
            x = input("Continue with JSON fetch? ")
            try: 
                if(sanitize_input(x) == "no"):
                    return
                else:
                    return(folder_name)
            except:
                print("Input not recognized.")
        else:
            return(folder_name)

# Selector for .json file names
def test_case_to_json(test_case):
    tc = {
        1: "CVM Test Case 1 metric_CVMResults.json",
        2: "CVM Test Case 2_CVMResults.json",
        3: "CVM Test Case 3 Rev B_CVMResults.json",
        4: "CVM Test Case 4_CVMResults.json",
        5: "CVM Test Case 5_CVMResults.json",
        6: "CVM Test Case 6 Rev F_CVMResults.json",
        7: "CVM Test Case 7_CVMResults.json"
    }
    return tc.get(test_case)

# Selector for test case name
def test_case_to_string(test_case):
    tc = {
        1: "CVM Test Case 1 metric",
        2: "CVM Test Case 2",
        3: "CVM Test Case 3 Rev B",
        4: "CVM Test Case 4",
        5: "CVM Test Case 5",
        6: "CVM Test Case 6 Rev F",
        7: "CVM Test Case 7"
    }
    return tc.get(test_case)

# Loads LPSD and pulls json output of input test case
def get_json(test_case):

    options = Options()
    try:
        prefs = {'profile.default_content_setting_values.automatic_downloads': 1, \
             'download.default_directory' : ("C:\\Users\\e1176752\\Documents\\VSCode\\Projects\\LPSD\\LPSD\\Archive\\JSON\\" + generate_folder_location(test_case))}
        
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get("https://qa-lpsd.nvent.com/") #TODO: allow for production server testing
        #driver.get("https://lpsd.nvent.com/")

        try:
            search_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "autodeskSigninButton")))
            search_button.click()
            time.sleep(1)

            input_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "userName")))
            input_field.send_keys("greg.martinjak@nvent.com")
            
            submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "verify_user_btn")))
            submit_button.click()
            time.sleep(1)

            input_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"password")))
            input_field.send_keys("nVent!23")

            submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "btnSubmit")))
            submit_button.click()
            time.sleep(1)

            allow_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "allow_btn")))
            allow_button.click()
            time.sleep(10)
            
            #edit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//td[contains( text(), 'CVM Test Case 1 metric')]/following-sibling::td/button")))
            edit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//td[contains( text(), '" +test_case_to_string(test_case)+"')]/following-sibling::td/button")))
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

            if (test_case == 6):
                checkbox_elements = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "analysis_startanalysis_step1_selectall")))
                checkbox_elements.click()
                time.sleep(1)

            else:
                #checkbox_elements = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "analysis-startanalysis-step1-model")))
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
            #//*[@id="userProjectsTable_Body"]/tr[388]/td[3]/button
            #<td class="table-project-name">CVM Test Case 1 metric</td>


        finally:
            driver.quit()
    except:
        print("Not acquiring JSON files.")
