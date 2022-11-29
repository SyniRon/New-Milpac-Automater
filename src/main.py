"""Main program file."""

import getpass

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)


driver = webdriver.Chrome(options=chrome_options)
print("Opening Browser")
driver.get("https://7cav.us/")
print("Trying to Login")


def ele_int(ele_type, ele, int_type, load=""):
    """Click eleement given.

    Args:
        ele_type (string): type of element to be clicked
        ele (string): element to be clicked
        int_type (int): type of interaction
        1 = click
        2 = send keys
        3 = select from dropdown list
        load (string): payload if needed
    """
    try:
        int_it = WebDriverWait(driver, timeout=10).until(
            lambda d: d.find_element(ele_type, ele)
        )
        if int_type == 1:
            int_it.click()
        elif int_type == 2:
            int_it.clear()
            int_it.send_keys(load)
        elif int_type == 3:
            select = Select(int_it)
            select.select_by_visible_text(load)
        else:
            print("Invalid interaction type sent")
    except TimeoutError:
        print("Element not found in time")


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
        driver.find_element("xpath", '//*[@id="js-XFUniqueId2"]/div/div[1]')
    except NoSuchElementException:
        print("2FA Confirmed")
    else:
        print("Incorrect 2FA Code")
        ele_int("xpath", '//*[@id="js-XFUniqueId2"]/div/div[1]/a', 1)
        two_fa(driver)


def milpac_nav(driver):
    """Navigates to milpac.

    Args:
        driver (webdriver)): chosen webdriver
    """
    ele_int(
        "xpath",
        '//*[@id="top"]/div[3]/div[2]/div[2]/div/nav/div/div[2]/div/ul/li[2]/div/a',
        1,
    )


def milpac_create(driver):
    """Create new milpac from user entry.

    Args:
        driver (webdriver): chosen webdriver
    """
    ele_int(
        "xpath",
        '//*[@id="top"]/div[3]/div[2]/div[5]/div/div/div[2]\
            /div[1]/div/div/a',
        1,
    )
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
        milpac_nav(driver)
    else:
        print("Milpac Successfully Created")


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


milpac_nav(driver)
milpac_create(driver)
milpac_confirm(driver)
