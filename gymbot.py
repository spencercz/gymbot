# so the damn freshmen stop reserving all the gym slots within 1 minute -spencer

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
import re

_CSS_SELECTORS = {
    "reserve time" : "div.col-lg-3:nth-child(4) > a:nth-child(1) > span:nth-child(2)",
    "lower floor"  : "div.list-group-item:nth-child(2) > div:nth-child(1) > div:nth-child(2)",
    "CAS"          : ".btn-linkedin",
    "login"        : "#itwd-cas-netid > button:nth-child(5)",
    "timeslot"     : "div.col-sm-6:nth-child(13) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > button:nth-child(1)",
    "modal close"   : "#btnModalClose > span:nth-child(1)"
}

choice = input("Select your browser:\n1) Firefox\n2) Chrome\n3) Safari\n")
if choice == '1':
    driver = webdriver.Firefox()
    print("Firefox selected")
elif choice == '2':
    driver = webdriver.Chrome()
    print("Chrome selected")
elif choice == '3':
    driver = webdriver.Safari()
    print("Safari selected")
else:
    print("Invalid response, exiting...")
    quit()

def setup():
    '''
    Opens the website, logs in the user, navigates to the workout time reservation, and chooses the lower floor
    '''
    user = input("Enter your UDel username/email\n")
    password = input("Enter your UDel password (don't worry, we won't keep this)\n")
    driver.get("https://recreation.udel.edu/")
    driver.maximize_window()
    # Login
    driver.find_element_by_id("loginLink").click()
    if check_exists_by_id(driver, "btnModalClose"):
        driver.find_element_by_css_selector(_CSS_SELECTORS["modal close"]).click()
    driver.find_element_by_css_selector(".btn-linkedin").click()
    driver.find_element_by_id("udelnetid").send_keys(user)
    driver.find_element_by_id("pword").send_keys(password)
    driver.find_element_by_css_selector(_CSS_SELECTORS["login"]).click()
    if check_exists_by_id(driver, "verification"):
        WebDriverWait(driver, 30000).until(check_exists_by_css(driver, _CSS_SELECTORS["reserve time"])) # wait for 2fa
    driver.find_element_by_css_selector(_CSS_SELECTORS["reserve time"]).click()
    driver.find_element_by_css_selector(_CSS_SELECTORS["lower floor"]).click()

def signup():
    button_exists = False
    while not button_exists:
        driver.refresh()
        button_exists = check_exists_by_css(driver, _CSS_SELECTORS["timeslot"])
    driver.find_element_by_css_selector(_CSS_SELECTORS["timeslot"]).click()
    driver.find_element_by_id("checkoutButton").click()

def check_times(driver):
    _TIMES = []
    for i in range(1, 99, 2):
        if i == 1:
            _TIMES.append(driver.find_element_by_css_selector("div.col-md-4:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > small:nth-child(1)").text.split('\\', 1)[0])
        else:
            try:
                _TIMES.append(driver.find_element_by_css_selector(f"div.col-sm-6:nth-child({i}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > small:nth-child(1)").text)
            except:
                pass
    return _TIMES

def check_buttons(driver):
    _BUTTONS = []
    for i in range(1, 99, 2):
        if i == 1:
            _BUTTONS.append(check_exists_by_css_bool(driver, "div.col-md-4:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(4)"))
        else:
            try:
                _BUTTONS.append(check_exists_by_css_bool(driver, f"div.col-sm-6:nth-child({i}) > div:nth-child(1) > div:nth-child(1) > a:nth-child(4)"))
            except:
                pass
    return _BUTTONS

def make_map():
    _TIMES = check_times(driver)
    _BUTTONS = check_buttons(driver)
    _MAP = {}
    for i in range(len(_TIMES)):
        _MAP[_TIMES[i]] = _BUTTONS[i]
    return _MAP

def check_exists_by_id(driver, id):
    try:
        driver.find_element_by_id(id)
    except NoSuchElementException:
        return False
    return True

def check_exists_by_css(driver, css):
    def _predicate(driver):
        try:
            driver.find_element_by_css_selector(css)
        except NoSuchElementException:
            return False
        return True
    return _predicate

def check_exists_by_css_bool(driver, css):
    try:
        driver.find_element_by_css_selector(css)
    except NoSuchElementException:
        return False
    return True

setup()
driver.get("https://recreation.udel.edu/Program/GetProgramDetails?courseId=b17a03e9-3f10-4f67-8bb2-c25372bfdc7d&semesterId=f12e0ccc-c5aa-4a59-a1bc-bdcb7ff3dfc0")
print(make_map())