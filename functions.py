from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def loginAttempt(driver):
    # request and store login credentials
    username = input("Enter 7cav.us Username(email):")
    password = input("Enter 7cav.us Password:")
    try:
        driver.find_element(
            'xpath', '//*[@id="top"]/div[2]/div[2]/div[2]/div/nav/div/div[3]/div[1]/a[1]'
        )
    except:
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
    except:
        print("Logged in")
    else:
        print("Invalid Username or Password Detected")
        loginAttempt()
        
def twoFa(driver):
    WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((
        By.CLASS_NAME, 'input'
    )))
    twoFaField = driver.find_element(
        By.CLASS_NAME, 'input'
    )
    twofacode = input("Enter 2FA Code:")
    twoFaField.clear()
    twoFaField.send_keys(twofacode)
    twofaconfirm = driver.find_element(
        By.CLASS_NAME, 'button--primary button button--icon button--icon--login'
    )
    twofaconfirm.click()
    try:
        driver.find_element(
            'xpath', '//*[@id="js-XFUniqueId2"]/div/div[1]'
        )
    except:
        print("2FA Confirmed")
    else:
        print("Incorrect 2FA Code")
        closeTwoFaWarning = driver.find_element(
            'xpath', '//*[@id="js-XFUniqueId2"]/div/div[1]/a'
        )
        closeTwoFaWarning.click()
        twoFa(driver)