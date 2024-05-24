from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import logging
import time
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
AUTODESK_USERNAME = os.getenv('AUTODESK_USERNAME')
NVENT_USERNAME = os.getenv('NVENT_USERNAME')
NVENT_PASSWORD = os.getenv('NVENT_PASSWORD')

def backup_lpsd():
    logger = logging.getLogger('selenium')
    # Generate a folder
    folder_location = "C:/Users/e1176752/Downloads/"
    folder_name = datetime.datetime.now().strftime("%Y-%m-%d")

    directory_name = folder_location + folder_name
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
        print(f"Directory '{directory_name}' created successfully.")
    else:
        print(f"Directory '{directory_name}' already exists")
        x = input("Continue with backup? ")
        try: 
            if(sanitize_input(x) == "no"):
                return
        except:
            print("Proceeding.")
        
    service = Service()
    #options = webdriver.ChromeOptions()
    options = Options()
    prefs = {'profile.default_content_setting_values.automatic_downloads': 1, \
            'download.default_directory' : ("C:\\Users\\e1176752\\Downloads\\" + folder_name)}

    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    driver = webdriver.Chrome(service=service, options=options)
    
    #driver.get("https://qa-lpsd.nvent.com")
    #driver.get("https://qa-lpsd.nvent.com/api/v1/administration")
    driver.get("https://lpsd.nvent.com/")
    time.sleep(5)

    json_exports = ["administration_admin_data_export_button", "administration_components_data_export_button", "administration_assembly_data_export_button", \
                    "administration_bim360projects_data_export_button",  "administration_pricing_export_button", \
                        "administration_revit_details_export_button", "administration_saved_projects_file_export_button", \
                            "administration_sfdc_mappings_file_export_button", "administration_sfdc_queue_file_export_button", \
                                "administration_shared_parameters_export_button", "administration_analysis_notes_export_button", \
                                    "administration_bom_notes_export_button"]

    try:
        search_button = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "autodeskSigninButton")))
        search_button.click()
        time.sleep(1)

        input_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "userName")))
        input_field.send_keys(AUTODESK_USERNAME)
        
        submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "verify_user_btn")))
        submit_button.click()
        time.sleep(3)

        # Updated due to SSO as of 04.16.2024
        input_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"i0116")))
        input_field.send_keys(NVENT_USERNAME)
        time.sleep(1)

        next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "idSIButton9")))
        next_button.click()
        time.sleep(1)

        input_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"i0118")))
        input_field.send_keys(NVENT_PASSWORD)
        time.sleep(1)

        next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "idSIButton9")))
        next_button.click()
        time.sleep(1)

        time.sleep(60)
        """
        input_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"password")))
        input_field.send_keys("nVent!23")

        submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "btnSubmit")))
        submit_button.click()
        time.sleep(1)
        """
        allow_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "allow_btn")))
        allow_button.click()
        time.sleep(10)

        adminportal_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "adminPortalLink")))
        adminportal_button.click()
        time.sleep(20)

        for string in json_exports:
            print("looking for {}".format(string))
            export = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, string)))
            export.click()
            time.sleep(1)
        
        time.sleep(30)


    finally:
        driver.quit()

def sanitize_input(input_str):

    if input_str == "Yes" or input_str == "YES" or input_str == "yEs":
        return "yes"
    elif input_str == "No" or input_str == "NO" or input_str == "no":
        return "no"
    else:
        raise
