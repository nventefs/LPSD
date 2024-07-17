from selenium import webdriver
from selenium.webdriver.edge.options import Options
from tester_functions import *
import constants
import os
from dotenv import load_dotenv
import pyotp
import time
load_dotenv()
AUTODESK_USERNAME = os.getenv('AUTODESK_USERNAME')
NVENT_USERNAME = os.getenv('NVENT_USERNAME')
NVENT_PASSWORD = os.getenv('NVENT_PASSWORD')
TWO_FACTOR_KEY = os.getenv('TWO_FACTOR_KEY')

class LPSDDriver(webdriver.Edge):
    def __init__ (self, type):
        self.configure_webdriver(type)
        self.active = False
        super().__init__(options=self.options)
        self.get("https://qa-lpsd.nvent.com/")
        self.login()
        time.sleep(6)
        self.associated_test = 0
    
    # fills in the options for the webdriver
    # sets default window size and download folder
    def configure_webdriver(self, type):
        self.options = Options()
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
        self.options.add_experimental_option("prefs", prefs)
        self.options.add_argument("--window-size=500,650")
        self.options.add_argument("--disable-popup-blocking")

    #Function to login to the website. May differ between users
    def login(self):
        totp = pyotp.TOTP(TWO_FACTOR_KEY)
        click_element(self, (By.ID, "autodeskSigninButton"))
        time.sleep(2)
        choose_textbox_value(self, (By.ID, "userName"), [AUTODESK_USERNAME])
        click_element(self, (By.ID, "verify_user_btn"))
        time.sleep(5)
        try:
            self.find_element(By.ID, "idTxtBx_SAOTCC_OTC")
            choose_textbox_value(self, (By.ID, "idTxtBx_SAOTCC_OTC"), [totp.now()])
            click_element(self, (By.ID, "idSubmit_SAOTCC_Continue"))
        except:
            click_element(self, (By.ID, "allow_btn"))
