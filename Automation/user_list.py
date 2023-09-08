from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pygetwindow as gw
import cv2
import xlsxwriter
import pyautogui
import pandas as pd
import csv
import time
import datetime
import os

# creates a folder in USERS folder with date, if folder exists returns date format
def generate_folder_location():

    folder_location = "C:/Users/e1176752/Documents/VSCode/Projects/LPSD/LPSD/Archive/USERS/"
    folder_name = datetime.datetime.now().strftime("%Y-%m-%d")

    directory_name = folder_location + folder_name
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
        print(f"Directory '{directory_name}' created successfully.")
    else:
        print(f"Directory '{directory_name}' already exists")
    return(folder_name)

# downloads userlist from BIM360 and puts it in USERS folder
#TODO: rename field names to coorespond to what they're actually searching for
def get_bim_users():
    if os.path.exists("C:\\Users\\e1176752\\Documents\\VSCode\\Projects\\LPSD\\LPSD\\Archive\\USERS\\" + generate_folder_location() + "\\BIM360_Members.csv"):
        print("BIM360 file already exists!")
        return
    
    options = Options()

    try:
        prefs = {'profile.default_content_setting_values.automatic_downloads': 1, \
             'download.default_directory' : ("C:\\Users\\e1176752\\Documents\\VSCode\\Projects\\LPSD\\LPSD\\Archive\\USERS\\" + generate_folder_location())}
                
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get("https://b2.autodesk.com/login")

        try:
            search_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "primary_button")))
            search_button.click()
            time.sleep(1)

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
        except:
            raise

    except:
        raise

# loads bim360 csv file into memory and returns the data
def load_bim_data(folder_location = "C:/Users/e1176752/Documents/VSCode/Projects/LPSD/LPSD/Archive/USERS/"):
    folder_name = datetime.datetime.now().strftime("%Y-%m-%d")
    directory_name = folder_location + folder_name + "/"

    if not os.path.exists(directory_name):
        print(f"Directory '{directory_name}' does not exist!")
        raise
    else:
        print(f"Directory '{directory_name}' found!")
    
    csv_file = directory_name + "BIM360_Members.csv"
    
    rows = []

    with open(csv_file, newline = '') as csvfile:
        csv_object = csv.reader(csvfile, delimiter = ',')
        for row in csv_object:
            rows.append(row)
        return rows, len(rows)

def to_excel(sheetname, data, writer):
    df = pd.DataFrame(data)
    df.columns = ["Email", "Status"]
    df.to_excel(writer, sheet_name = sheetname, index = False)

# retrieves the LPSD users list in outlook and saves as csv file
def get_outlook_list():
    if os.path.exists("C:\\Users\\e1176752\\Documents\\VSCode\\Projects\\LPSD\\LPSD\\Archive\\USERS\\" + generate_folder_location() + "\\LPSEDUsers_Outlook.csv"):
        print("Outlook file already exists!")
        return
    outlookwindow = get_outlookwindow()
    outlookwindow.maximize()
    outlookwindow.moveTo(0,0
                         )
    outlookwindow.activate()
    time.sleep(2)
    coords = pyautogui.locateOnScreen("C:/Users/e1176752/Documents/VSCode/Projects/LPSD/LPSD/Automation/img/contacts.png", confidence = 0.65)
    pyautogui.click(coords[0], coords[1])
    time.sleep(2.5)
    pyautogui.press('alt'),     time.sleep(0.75)
    pyautogui.press('f'),       time.sleep(0.5)
    pyautogui.press('o'),       time.sleep(0.5)
    pyautogui.press('i'),       time.sleep(0.5) # Import/export screen
    pyautogui.press('up'),      time.sleep(0.5)
    pyautogui.press('up'),      time.sleep(0.5)
    pyautogui.press('up'),      time.sleep(0.5) # Select file output
    pyautogui.press('enter'),   time.sleep(0.5) # Export to file
    pyautogui.press('enter'),   time.sleep(0.5) # Comma seperated values
    coords = pyautogui.locateOnScreen("C:/Users/e1176752/Documents/VSCode/Projects/LPSD/LPSD/Automation/img/LPSDUsers.png", confidence = 0.65)
    pyautogui.click(coords[0], coords[1])
    time.sleep(2.5)
    #pyautogui.press('down'),    time.sleep(0.5)
    #pyautogui.press('down'),    time.sleep(0.5)
    #pyautogui.press('down'),    time.sleep(0.5)
    #pyautogui.press('down'),    time.sleep(0.5)
    #pyautogui.press('down'),    time.sleep(0.5)
    pyautogui.press('enter'),   time.sleep(0.5)
    pyautogui.write('C:\\Users\\e1176752\\Documents\\VSCode\\Projects\\LPSD\\LPSD\\Archive\\USERS\\' + generate_folder_location() + '\\LPSDUsers_Outlook.csv'), time.sleep(1)
    pyautogui.press('enter'),   time.sleep(1)
    pyautogui.press('enter'),   time.sleep(1)
    time.sleep(4)

# returns the name of the outlook window for gw
def get_outlookwindow():
    temp = gw.getAllTitles()
    for k in temp:
        if k.find('Outlook') > 1:
            print(k)
            return gw.getWindowsWithTitle(k)[0]

# loads outlook csv file into memory and returns the data
def load_outlook_data(folder_location = "C:/Users/e1176752/Documents/VSCode/Projects/LPSD/LPSD/Archive/USERS/"):
    folder_name = datetime.datetime.now().strftime("%Y-%m-%d")
    directory_name = folder_location + folder_name + "/"

    if not os.path.exists(directory_name):
        print(f"Directory '{directory_name}' does not exist!")
        raise
    else:
        print(f"Directory '{directory_name}' found!")
    
    csv_file = directory_name + "LPSDUsers_Outlook.csv"
    
    rows = []
    with open(csv_file, newline = '') as csvfile:
        csv_object = csv.reader(csvfile, delimiter = ',')
        for row in csv_object:
            rows.append(row)
        return rows, len(rows)

# Retreive outlook data from outlook, creates list of first.lastname@nvent.com
outlook_list = []
get_outlook_list()
outlook_data = load_outlook_data()
for k in range(1,outlook_data[1]):
    left = outlook_data[0][k][59].find('(')
    right = outlook_data[0][k][59].find(')')
    outlook_list.append(outlook_data[0][k][59][left+1:right])
    
# Retreive BIM360 user data from BIM360, creates list of users 
active_bim_user_list = []
inactive_bim_user_list = []
get_bim_users()
bim_data = load_bim_data()

# Seperate BIM360 users into active/inactive
for k in range(1,bim_data[1]):
    if bim_data[0][k][7] == 'Active':
        active_bim_user_list.append([bim_data[0][k][0], bim_data[0][k][7]])
    else:
        inactive_bim_user_list.append([bim_data[0][k][0], bim_data[0][k][7]])

# Determine if any BIM360 active users are not in LPSD outlook list
changes = []
for k in active_bim_user_list:
    temp = 0
    for j in outlook_list:
        if j.lower() == k[0].lower():
            temp = 1
    if (temp == 0):
        print("User " + k[0] + " not found in outlook list.")
        changes.append(k[0])
        

"""
# Write to file UserList.xlsx the received information
filename = "C:/Users/e1176752/Documents/VSCode/Projects/LPSD/LPSD/Archive/USERS/" + generate_folder_location() + '/UserList.xlsx'
print(filename)
writer = pd.ExcelWriter(filename, engine = 'xlsxwriter')
to_excel('Active', active_bim_user_list, writer)
to_excel('Inactive', inactive_bim_user_list, writer)
to_excel('Changes', changes, writer)
writer.save()
"""