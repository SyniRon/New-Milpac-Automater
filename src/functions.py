import getpass
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# this function is called if the user is not already logged in
# it collects the login data from the user and uses it to log in to the site
# TODO: Add gui for login credential collection
# TODO: Add option to securely store login credentials


def loginAttempt(driver):
    username = input("Enter 7cav.us Username(email):")
    password = getpass.getpass(prompt="Enter 7cav.us Password:")
    try:
        driver.find_element(
            'xpath', '//*[@id="top"]/div[2]/div[2]/div[2]/div/nav/div/div[3]/div[1]/a[1]'
        )
    except Exception:
        print("Retrying Login")
    else:
        print("Loggin In")
        loginButton = driver.find_element(
            'xpath', '//*[@id="top"]/div[2]/div[2]/div[2]/div/nav/div/div[3]/div[1]/a[1]'
        )
        loginButton.click()
        WebDriverWait(driver, timeout=10).until(EC.element_to_be_clickable((
            By.XPATH, '//*[@id="js-XFUniqueId5"]/div/div[2]/div/div/div/div/dl/dd/ul/li/a'
        )))
        keyCloakButton = driver.find_element(
            'xpath', '//*[@id="js-XFUniqueId5"]/div/div[2]/div/div/div/div/dl/dd/ul/li/a'
        )
        keyCloakButton.click()
    WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((
        By.XPATH, '//*[@id="username"]'
    )))
    emailField = driver.find_element(
        'xpath', '//*[@id="username"]'
    )
    passwordField = driver.find_element(
        'xpath', '//*[@id="password"]'
    )
    loginButton2 = driver.find_element(
        'xpath', '//*[@id="kc-login"]'
    )
    emailField.clear()
    emailField.send_keys(username)
    passwordField.clear()
    passwordField.send_keys(password)
    loginButton2.click()
    try:
        driver.find_element(
            'xpath', '//*[@id="kc-content-wrapper"]/div[1]'
        )
    except Exception:
        print("Logged in")
    else:
        print("Invalid Username or Password Detected")
        loginAttempt(driver)

# this function is called if 2FA is detected, it requests the 2FA code and then submits it and completes login
# TODO: Add gui for 2FA code collection


def twoFa(driver):
    WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((
        By.NAME, 'code'
    )))
    twoFaField = driver.find_element(
        By.NAME, 'code'
    )
    twofacode = input("Enter 2FA Code:")
    twoFaField.clear()
    twoFaField.send_keys(twofacode)
    twofaconfirm = driver.find_element(
        By.XPATH, '//*[@id="top"]/div[2]/div[2]/div[6]/div/div/div[2]/div[2]/form/div/dl/dd/div/div[2]/button'
    )
    twofaconfirm.click()
    try:
        driver.find_element(
            'xpath', '//*[@id="js-XFUniqueId2"]/div/div[1]'
        )
    except Exception:
        print("2FA Confirmed")
    else:
        print("Incorrect 2FA Code")
        closeTwoFaWarning = driver.find_element(
            'xpath', '//*[@id="js-XFUniqueId2"]/div/div[1]/a'
        )
        closeTwoFaWarning.click()
        twoFa(driver)
