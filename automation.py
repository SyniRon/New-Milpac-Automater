from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from functions import loginAttempt
from functions import twoFa
chrome_options = Options() 
chrome_options.add_experimental_option("detach", True)


# open webdriver browser
driver = webdriver.Chrome(options=chrome_options)
print("Opening Browser")
driver.get('https://7cav.us/')
print("Opened")
# attempt to login
print("Trying to Login")
# this function performs login using previously acquired details

        
try: 
    driver.find_element(
        'xpath', '//*[@id="top"]/div[2]/div[2]/div[2]/div/nav/div/div[3]/div[1]/a[1]'
    )
except: 
    print("Already Logged In")
else:
    loginAttempt(driver)

try:
    driver.find_element(
        'xpath', '//*[@id="top"]/div[2]/div[2]/div[6]/div/div/div[2]/div[2]/form/div/div/dl[3]/dd/ul/li/label/span'
    )
except:
    print("2FA Not Detected, skipping")
else:
    print("2FA Required")
    twoFa(driver)
    