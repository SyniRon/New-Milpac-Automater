from functions import loginAttempt, twoFa, milpacNav, milpacCreate
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# this calls the webdriver for chrome and brings up the 7cav site
# TODO: add options for more browsers
# TODO: build gui for app
driver = webdriver.Chrome(options=chrome_options)
print("Opening Browser")
driver.get("https://7cav.us/")
print("Trying to Login")

try:
    driver.find_element(
        "xpath", '//*[@id="top"]/div[2]/div[2]/div[2]/div/nav/div/div[3]/div[1]/a[1]'
    )
except Exception:
    print("Already Logged In")
else:
    loginAttempt(driver)

try:
    driver.find_element(
        "xpath",
        '//*[@id="top"]/div[2]/div[2]/div[6]/div/div/div[2]/div[2]/form/div/div/dl[3]/dd/ul/li/label/span',
    )
except Exception:
    print("2FA Not Detected, skipping")
else:
    print("2FA Required")
    twoFa(driver)

milpacNav(driver)
milpacCreate(driver)
