"""Main program file."""

import getpass
import time
import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

# testing code to make browser stay open after runtime completion
# TODO: remove testing code and make headless
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# set driver to use selected options
driver = webdriver.Chrome(options=chrome_options)
# testing code while browser isn't headless
# TODO: remove irrelevant size code once browser is headless
driver.set_window_size(1024, 768)
print("Opening Browser")
driver.get("https://7cav.us/")
print("Trying to Login")


def ele_int(ele_type, ele, int_type, load=""):
    """Interact with given element in chosen way.

    Args:
        ele_type (string): type of element to be clicked
        ele (string): element to be clicked
        int_type (int): type of interaction
        1 = click
        2 = send keys
        3 = select from dropdown list
        load (string): payload if needed
    """
    # we are waiting to see if the element requested
    # exists or not and giving time for it to render
    # if it doesn't after 10 seconds a timeout is thrown
    int_it = WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element(ele_type, ele)
    )
    # if payload int is 1 we're clicking
    if int_type == 1:
        int_it.click()
    # if payload int is 2 we're sending keys
    elif int_type == 2:
        int_it.clear()
        int_it.send_keys(load)
    # if payload int is 3 we're selecing from a list
    elif int_type == 3:
        select = Select(int_it)
        select.select_by_visible_text(load)
    # if the payload has a bad int_type we error out
    else:
        raise ValueError("Invalid int_type selection")


def login_attempt(driver):
    """Automatic Site Login.

    Args:
        driver (webdriver): selenium webdriver
    """
    username = input("Enter 7cav.us Username(email):")
    password = getpass.getpass(prompt="Enter 7cav.us Password:")
    try:
        driver.find_element(
            "xpath",
            '//*[@id="top"]/div[2]/div[2]/div[2]/div\
                /nav/div/div[3]/div[1]/a[1]',
        )
    except NoSuchElementException:
        print("Retrying Login")
    else:
        confirm_login(driver)
    # input username
    ele_int("xpath", '//*[@id="username"]', 2, username)
    ele_int("xpath", '//*[@id="password"]', 2, password)
    ele_int("xpath", '//*[@id="kc-login"]', 1)
    try:
        driver.find_element("xpath", '//*[@id="kc-content-wrapper"]/div[1]')
    except NoSuchElementException:
        print("Logged in")
    else:
        print("Invalid Username or Password Detected")
        login_attempt(driver)


def confirm_login(driver):
    """Finishes Login.

    Args:
        driver (webdriver): chosen webdriver
    """
    print("Logging In")
    ele_int(
        "xpath", '//*[@id="top"]/div[2]/div[2]/div[2]/div/nav/div/div[3]/div[1]/a[1]', 1
    )
    ele_int(
        "xpath",
        '//*[@id="js-XFUniqueId5"]/div/div[2]/div/div/div/div/dl/dd\
                    /ul/li/a',
        1,
    )


def two_fa(driver):
    """Handle 2fa entry.

    Args:
        driver (webdriver): selected webdriver
    """
    # requests 2FA code from user and stores to variable
    two_fa_code = input("Enter 2FA Code:")
    # scroll to bottom of page to avoid click intercept
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # enters 2FA code into box
    ele_int("name", "code", 2, two_fa_code)
    # clicks confirm button
    ele_int(
        "xpath",
        '//*[@id="top"]/div[2]/div[2]/div[6]/div/div/div[2]/div[2]/form/div\
            /dl/dd/div/div[2]/button',
        1,
    )
    try:
        WebDriverWait(driver, timeout=1).until(ec.url_matches("https://7cav.us/"))
    except TimeoutError:
        print("Incorrect 2FA Code")
        ele_int("xpath", '//*[@id="js-XFUniqueId2"]/div/div[1]/a', 1)
        two_fa(driver)
    else:
        print("2FA Confirmed")


def milpac_create(driver):
    """Create new milpac on combat roster from user entry.

    Args:
        driver (webdriver): chosen webdriver
    """
    time.sleep(0.5)
    driver.get("https://7cav.us/rosters/1/add-user")
    # waits for create milpac page to load
    WebDriverWait(driver, timeout=10).until(
        ec.presence_of_element_located(
            (
                By.XPATH,
                '//*[@id="top"]/div[3]/div[2]/div[5]/div\
                    /div/div[2]/div[2]/div/h1',
            )
        )
    )
    # requests current username, new username, real name, join date
    milpac_username = input("Enter current forum username:")
    milpac_username_update = input("Update username to the following:")
    milpac_real_name = input("Enter Real Name:")
    milpac_join_date = input("Enter Join Date (YYYY-MM-DD):")
    # uses above input to fill out new milpac creation fields
    ele_int("name", "username", 2, milpac_username)
    ele_int(
        "xpath",
        '//*[@id="top"]/div[3]/div[2]/div[5]/div/div/div[2]/div[3]\
            /form/div/div/dl[2]/dd/ul/li/label/i',
        1,
    )
    ele_int("name", "new_username", 2, milpac_username_update)
    ele_int("name", "real_name", 2, milpac_real_name)
    ele_int("name", "rank_id", 3, "Recruit")
    ele_int("name", "position_id", 3, "New Recruit")
    ele_int("name", "custom_fields[joinDate]", 2, milpac_join_date)
    ele_int("name", "custom_fields[promoDate]", 2, milpac_join_date)


def milpac_confirm(driver):
    """Confirm Milpac Created Succesfully.

    Args:
        driver (webdriver): selected webdriver
    """
    # clicks the confirm button twice
    # why? v0v but it wont work otherwise
    # i think the calendar covers the button
    for _ in range(2):
        ele_int(
            "xpath",
            '//*[@id="top"]/div[3]/div[2]/div[5]/div/div/\
            div[2]/div[3]/form/dl/dd/div/div[2]/button',
            1,
        )
    # waits to make sure no errors are returned, if they are repeats the whole process
    # might be cool if we could figure out the specific issue instead of starting over
    try:
        WebDriverWait(driver, timeout=10).until(
            ec.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="top"]/div[3]/div[2]/div[5]/div/div\
                        /div[2]/div[2]/div/div/div/div/button',
                )
            )
        )
    except NoSuchElementException:
        print("Invalid Data Entered, Try Again")
        ele_int("xpath", '//*[@id="js-XFUniqueId3"]/div/div[1]/a', 1)
        milpac_create(driver)
    else:
        print("Milpac Successfully Created")
        WebDriverWait(driver, timeout=10).until(
            ec.url_contains("https://7cav.us/rosters/profile/?unique_id=")
        )
        return driver.current_url


def milpac_puc_add(driver, created_milpac):
    """Add Pres Unit Citation awards to created milpac.

    Args:
        driver (webdriver): chosen webdriver
        created_milpac (string): url of created milpac
    """
    # grab user id of milpac to add pucs to
    u_id = created_milpac.replace("https://7cav.us/rosters/profile/?unique_id=", "")
    # paths are media/puc1-6.jpg
    # build dictionary of files to upload
    puc_dict = {
        "/media/puc1.jpg": "2003-03-18",
        "/media/puc2.jpg": "2004-09-01",
        "/media/puc3.jpg": "2009-08-10",
        "/media/puc4.jpg": "2010-09-18",
        "/media/puc5.jpg": "2011-06-02",
        "/media/puc6.jpg": "2021-05-16",
    }
    # iterate through dict to add each puc
    for puc_img, puc_date in puc_dict.items():
        # navigate to add award page for the milpac
        driver.get(f"https://7cav.us/rosters/1/awards/add?unique_id={u_id}")
        # sleep a moment to let the page load
        time.sleep(0.2)
        # select the award name
        ele_int("name", "award_id", 3, "Army & Air Force Presidential Unit Citation")
        # input the award date
        ele_int("name", "award_date", 2, puc_date)
        # upload the correct file
        ele_int("name", "upload", 2, os.getcwd() + puc_img)
        # click the calendar button to make it go away
        ele_int(
            "xpath",
            '//*[@id="top"]/div[3]/div[2]/div[5]/div/div/div[2]/div[3]/form/div/div/dl\
                [3]/dd/div/span',
            1,
        )
        # click the save button
        ele_int(
            "xpath",
            '//*[@id="top"]/div[3]/div[2]/div[5]/div/div/div[2]/div[3]/form/div/dl/dd/\
                div/div[2]/button',
            1,
        )
        # wait a sec for site loading
        time.sleep(0.2)


try:
    driver.find_element("xpath", '//*[@id="XF"]/body/div[2]/ul/li/div/div[2]/a[1]')
except NoSuchElementException:
    pass
else:
    ele_int("xpath", '//*[@id="XF"]/body/div[2]/ul/li/div/div[2]/a[1]', 1)


try:
    driver.find_element(
        "xpath", '//*[@id="top"]/div[2]/div[2]/div[2]/div/nav/div/div[3]/div[1]/a[1]'
    )
except NoSuchElementException:
    print("Already Logged In")
else:
    login_attempt(driver)

try:
    driver.find_element(
        "xpath",
        '//*[@id="top"]/div[2]/div[2]/div[6]/div/div/div[2]/div[2]/form/div\
            /div/dl[3]/dd/ul/li/label/span',
    )
except NoSuchElementException:
    print("2FA Not Detected, skipping")
else:
    print("2FA Required")
    two_fa(driver)


milpac_create(driver)
created_milpac = milpac_confirm(driver)
milpac_puc_add(driver, created_milpac)
