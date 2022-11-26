"""Main program file."""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

from functions import (login_attempt, milpac_confirm, milpac_create,
                       milpac_nav, two_fa)

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# this calls the webdriver for chrome and brings up the 7cav site


driver = webdriver.Chrome(options=chrome_options)
print("Opening Browser")
driver.get("https://7cav.us/")
print("Trying to Login")

try:
    driver.find_element(
        "xpath",
        '//*[@id="top"]/div[2]/div[2]/div[2]/div/nav/div/div[3]/div[1]/a[1]'
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
