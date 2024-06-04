import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

#Function to login to the website. May differ between users
def login(driver: webdriver.Edge, username):
    click_element(driver, (By.ID, "autodeskSigninButton"))
    time.sleep(1)
    choose_textbox_value(driver, (By.ID, "userName"),[username])
    click_element(driver, (By.ID, "verify_user_btn"))
    click_element(driver, (By.ID, "allow_btn"))

# chooses a combobox value. Can be from all possible options or from a list of user-defined options
# TODO: add support for 'first' and 'last' choice options
def choose_combobox_value(driver: webdriver.Edge, selection, allow_empty_value = False, choice = "random", manual_values: list = None):
    try:
        dropdown_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(selection))
        dropdown = Select(dropdown_element)

        if choice == "random":
            choice = random.choice(dropdown.options).text
            if not allow_empty_value:
                while choice == "":
                    choice = random.choice(dropdown.options).text
        elif choice == "manual":
            choice = random.choice(manual_values)

        dropdown.select_by_visible_text(choice)
        return choice
    except:
        print("No combobox value could be chosen for " + str(selection))
        return None

#Chooses a random value from the list argument to put into the textbox.
#A list with only one element can be used for a direct input value
def choose_textbox_value(driver: webdriver.Edge, selection, list):
    try:
        choice = random.choice(list)
        textbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(selection))
        textbox.click()
        ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
        textbox.send_keys(choice)
        return choice
    except:
        print("No textbox value could be chosen for "+ str(selection))

# Reads the text from an element found by selection
def read_value(driver: webdriver.Edge, selection):
    try:
        element = driver.find_element(selection[0], selection[1])
        return element.get_attribute("value")
    except:
        print("value from " + str(selection) + " could not be read")

# clicks the element found by selection
# supports multiple elements found by the selection, can click element at element_index
def click_element(driver: webdriver.Edge, selection, multiple = False, element_index = 0):
    try:
        if multiple:
            elements = driver.find_elements(selection[0], selection[1])
            selection = (By.ID, elements[element_index].get_attribute("id"))
        
        element = WebDriverWait(driver,10).until(EC.element_to_be_clickable(selection))
        element.click()
    except:
        print(str(selection) + " could not be clicked")

#dumps html of the current webpage to the file with the name provided
def dump_html_to_file(driver: webdriver.Edge, filename):
    with open(filename, 'w') as f:
        f.write(driver.page_source)