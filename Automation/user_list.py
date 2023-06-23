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

def get_bim_users():
    options = Options()

    try:
        prefs = {'profile.default_content_setting_values.automatic_downloads': 1, \
             'download.default_directory' : ("C:\\Users\\e1176752\\Documents\\VSCode\\Projects\\LPSD\\LPSD\\Archive\\USERS\\")}
                
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get("https://b2.autodesk.com/login")

        try:
            search_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "primary_button")))
            search_button.click()
            time.sleep(3)

            #print((driver.find_element(By.ID,"userName")))
            #print((driver.find_element(By.NAME,"UserName")))
            #print((driver.find_element(By.CLASS_NAME, "form-control customInput2")))
            #print((driver.find_element(By.XPATH, "//*[@id='userName']")))
            input_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "UserName")))
            input_field.send_keys("greg.martinjak@nvent.com")
            
            submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "verify_user_btn")))
            submit_button.click()
            time.sleep(1)

            input_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"password")))
            input_field.send_keys("nVent!23")

            submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "btnSubmit")))
            submit_button.click()
            time.sleep(1)

            allow_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "hq")))
            allow_button.click()
            #Tabs__tab-name
            
            allow_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/section/header/div/div/div[2]/div[1]/header/div[2]/a[2]/span")))
            allow_button.click()

            allow_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "more-actions-selector")))
            allow_button.click()
  
            allow_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='more-actions-selector']/ul/li[4]")))
            allow_button.click()


            print("we did it")
            time.sleep(10)
            time.sleep(100)
        except:
            raise

    except:
        raise

get_bim_users()