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


service = Service()
#options = webdriver.ChromeOptions()
options = Options()
prefs = {'profile.default_content_setting_values.automatic_downloads': 1, \
        'download.default_directory' : ("C:\\Users\\e1176752\\Downloads\\")}

options.add_experimental_option("prefs", prefs)
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://qa-lpsd.nvent.com")
#driver.get("https://qa-lpsd.nvent.com/api/v1/administration")
#driver.get("https://lpsd.nvent.com/")

while True:
    pass