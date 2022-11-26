"""Library of Functions."""

import getpass

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait


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
    WebDriverWait(driver, timeout=10).until(
        ec.presence_of_element_located((By.XPATH, '//*[@id="username"]'))
    )
    email_field = driver.find_element("xpath", '//*[@id="username"]')
    password_field = driver.find_element("xpath", '//*[@id="password"]')
    login_button2 = driver.find_element("xpath", '//*[@id="kc-login"]')
    email_field.clear()
    email_field.send_keys(username)
    password_field.clear()
    password_field.send_keys(password)
    login_button2.click()
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
    loginbutton = driver.find_element(
        "xpath",
        '//*[@id="top"]/div[2]/div[2]/div[2]/div/nav/div/div[3]/div[1]/a[1]',
    )
    loginbutton.click()
    WebDriverWait(driver, timeout=10).until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="js-XFUniqueId5"]/div/div[2]/div/div/div/div/dl/dd\
                    /ul/li/a',
            )
        )
    )
    key_cloak_button = driver.find_element(
        "xpath",
        '//*[@id="js-XFUniqueId5"]/div/div[2]/div/div/div/div/dl/dd/ul/li/a',
    )
    key_cloak_button.click()


def two_fa(driver):
    """Handle 2fa entry.

    Args:
        driver (webdriver): selected webdriver
    """
    WebDriverWait(driver, timeout=10).until(
        ec.presence_of_element_located((By.NAME, "code"))
    )
    two_fa_field = driver.find_element(By.NAME, "code")
    two_fa_code = input("Enter 2FA Code:")
    two_fa_field.clear()
    two_fa_field.send_keys(two_fa_code)
    two_fa_confirm = driver.find_element(
        By.XPATH,
        '//*[@id="top"]/div[2]/div[2]/div[6]/div/div/div[2]/div[2]/form/div\
            /dl/dd/div/div[2]/button',
    )
    two_fa_confirm.click()
    try:
        driver.find_element("xpath", '//*[@id="js-XFUniqueId2"]/div/div[1]')
    except NoSuchElementException:
        print("2FA Confirmed")
    else:
        print("Incorrect 2FA Code")
        close_two_fa_warning = driver.find_element(
            "xpath", '//*[@id="js-XFUniqueId2"]/div/div[1]/a'
        )
        close_two_fa_warning.click()
        two_fa(driver)


# this function finds the milpac link element on page and then navigates to it


def milpac_nav(driver):
    """Navigates to milpac.

    Args:
        driver (webdriver)): chosen webdriver
    """
    WebDriverWait(driver, timeout=10).until(
        ec.presence_of_element_located(
            (
                By.XPATH,
                '//*[@id="top"]/div[3]/div[2]/div[2]/div/nav/div/div[2]\
                    /div/ul/li[2]/div/a',
            )
        )
    )
    milpac_link = driver.find_element(
        By.XPATH,
        '//*[@id="top"]/div[3]/div[2]/div[2]/div/nav/div/div[2]\
            /div/ul/li[2]/div/a',
    )
    milpac_link.click()


def milpac_create(driver):
    """Create new milpac from user entry.

    Args:
        driver (webdriver): chosen webdriver
    """
    WebDriverWait(driver, timeout=10).until(
        ec.presence_of_element_located(
            (
                By.XPATH,
                '//*[@id="top"]/div[3]/div[2]/div[5]/div/div/div[2]\
                    /div[1]/div/div/a',
            )
        )
    )
    add_user_button = driver.find_element(
        "xpath", '//*[@id="top"]/div[3]/div[2]/div[5]/div/div/div[2]\
            /div[1]/div/div/a'
    )
    add_user_button.click()
    WebDriverWait(driver, timeout=10).until(
        ec.presence_of_element_located(
            (
                By.XPATH,
                '//*[@id="top"]/div[3]/div[2]/div[5]/div\
                    /div/div[2]/div[2]/div/h1',
            )
        )
    )
    milpac_username = input("Enter forum username:")
    milpac_username_update = input("Update username to the following:")
    milpac_real_name = input("Enter Real Name:")
    milpac_join_date = input("Enter Join Date:")
    milpac_username_update_entry = milpac_data_entry(
        driver, "username", milpac_username, "new_username"
        )

    milpac_username_update_checkbox = driver.find_element(
        By.XPATH,
        '//*[@id="top"]/div[3]/div[2]/div[5]/div/div/div[2]/div[3]\
            /form/div/div/dl[2]/dd/ul/li/label/i',
    )
    milpac_username_update_checkbox.click()
    milpac_username_update_entry.send_keys(milpac_username_update)
    milpac_rank_select = milpac_data_entry(
        driver, "real_name", milpac_real_name, "rank_id"
        )
    select = Select(milpac_rank_select)
    select.select_by_visible_text("Recruit")
    milpac_position_select = driver.find_element(By.NAME, "position_id")
    select = Select(milpac_position_select)
    select.select_by_visible_text("New Recruit")
    milpac_promotion_date_entry = milpac_data_entry(
        driver, "custom_fields[joinDate]",
        milpac_join_date, "custom_fields[promoDate]"
        )

    milpac_promotion_date_entry.send_keys(milpac_join_date)


def milpac_data_entry(driver, arg1, arg2, arg3):
    """Use args to find field and enter data.

    Args:
        driver (webdriver): chosen webdriver
        arg1 (element name): name of element to find
        arg2 (string): data to enter
        arg3 (element name): name of element to return

    Returns:
        element: returns selenium element
    """
    milpac_entry = driver.find_element(By.NAME, arg1)
    milpac_entry.send_keys(arg2)
    return driver.find_element(By.NAME, arg3)
