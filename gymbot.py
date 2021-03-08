# so that i can sign up for the gym without the slot filling up in 1 minute -spencer

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from getpass import getpass

_CSS_SELECTORS = {
    "reserve time"   : "div.col-lg-3:nth-child(4) > a:nth-child(1) > span:nth-child(2)",
    "lower floor"    : "div.list-group-item:nth-child(2) > div:nth-child(1) > div:nth-child(2)",
    "CAS"            : ".btn-linkedin",
    "login"          : "#itwd-cas-netid > button:nth-child(5)",
    "modal close"    : "#btnModalClose > span:nth-child(1)",
    "checkout popup" : "div.card-item-main:nth-child(3) > button:nth-child(1)"
}

_TIMESLOTS = {
    '1'  : '6:05 AM - 7:20 AM',
    '2'  : '7:30 AM - 8:45 AM',
    '3'  : '8:55 AM - 10:05 AM',
    '4'  : '10:15 AM - 11:30 AM',
    '5'  : '11:40 AM - 12:55 PM',
    '6'  : '1:05 PM - 2:15 PM',
    '7'  : '2:25 PM - 3:35 PM',
    '8'  : '3:45 PM - 4:55 PM',
    '9'  : '5:05 PM - 6:15 PM',
    '10' : '6:25 PM - 7:35 PM',
    '11' : '7:45 PM - 8:55 PM'
}

def setup():
    '''
    Opens the website, logs in the user, navigates to the workout time reservation, and chooses the lower floor
    '''
    user = input("UDel username/email: ")
    password = getpass()
    driver.get("https://recreation.udel.edu/")
    driver.maximize_window()
    # Login
    driver.find_element_by_id("loginLink").click()
    sleep(2)
    driver.find_element_by_css_selector(".btn-linkedin").click()
    driver.find_element_by_id("udelnetid").send_keys(user)
    driver.find_element_by_id("pword").send_keys(password)
    driver.find_element_by_css_selector(_CSS_SELECTORS["login"]).click()
    if check_exists_by_id(driver, "verification"):
        WebDriverWait(driver, 30000).until(check_exists_by_css(driver, _CSS_SELECTORS["reserve time"])) # wait for 2fa
    driver.find_element_by_css_selector(_CSS_SELECTORS["reserve time"]).click()
    driver.find_element_by_css_selector(_CSS_SELECTORS["lower floor"]).click()

def signup(choice):
    button_exists = False
    while not button_exists:
        driver.refresh()
        time_map = make_map()
        button_exists = time_map[_TIMESLOTS[choice]][0]
    driver.find_element_by_css_selector(time_map[_TIMESLOTS[choice]][1]).click()
    driver.find_element_by_id("checkoutButton").click()
    driver.find_element_by_css_selector(_CSS_SELECTORS["checkout popup"]).click()
    print("Time slot get!")

def check_times(driver):
    '''
    Helper function for make_map()
    '''
    _TIMES = []
    for i in range(1, 99, 2):
        if i == 1:
            _TIMES.append(driver.find_element_by_css_selector("div.col-md-4:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > small:nth-child(1)").text.split("\n", 1)[0])
        else:
            try:
                _TIMES.append(driver.find_element_by_css_selector(f"div.col-sm-6:nth-child({i}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > small:nth-child(1)").text.split("\n", 1)[0])
            except:
                pass
    return _TIMES

def check_buttons(driver):
    '''
    Helper function for make_map()
    '''
    _BUTTONS = []
    for i in range(1, 99, 2):
        if i == 1:
            _BUTTONS.append((check_exists_by_css_bool(driver, "div.col-md-4:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > button:nth-child(1)"), "div.col-md-4:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > button:nth-child(1)"))                                                           
        else:
            try:
                _BUTTONS.append((check_exists_by_css_bool(driver, f"div.col-sm-6:nth-child({i}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > button:nth-child(1)"), f"div.col-sm-6:nth-child({i}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > button:nth-child(1)"))                                                                 
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

if __name__ == "__main__":
    choice = int(input("Select your browser:\n1) Firefox\n2) Chrome\n3) Safari\n"))
    if choice == 1:
        driver = webdriver.Firefox()
        print("Firefox selected")
    elif choice == 2:
        driver = webdriver.Chrome()
        print("Chrome selected")
    elif choice == 3:
        driver = webdriver.Safari()
        print("Safari selected")
    else:
        print("Invalid response, exiting...")
        quit()
    choice = input("Select your desired timeslot:\n1) 6:05 AM - 7:20 AM\n2) 7:30 AM - 8:45 AM\n3) 8:55 AM - 10:05 AM\n4) 10:15 AM - 11:30 AM\n5) 11:40 AM - 12:55 PM\n6) 1:05 PM - 2:15 PM\n7) 2:25 PM - 3:35 PM\n8) 3:45 PM - 4:55 PM\n9) 5:05 PM - 6:15 PM\n10) 6:25 PM - 7:35 PM\n11) 7:45 PM - 8:55 PM\n")
    if int(choice) > 11 or int(choice) < 1:
        print("Invalid response, exiting...")
        quit()
    setup()
    signup(choice)
