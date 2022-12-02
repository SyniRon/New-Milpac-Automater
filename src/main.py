"""Main program file."""

import os
import time

import customtkinter as ctk
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
chrome_options.add_argument("--headless")
# chrome_options.add_experimental_option("detach", True)

# set driver to use selected options
driver = webdriver.Chrome(options=chrome_options)
# testing code while browser isn't headless
# TODO: remove irrelevant size code once browser is headless
# driver.set_window_size(1024, 768)
# opens the browser to 7cav.us
print("Opening Browser")
driver.get("https://7cav.us/")
print("Trying to Login")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.geometry("500x800")


def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()


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


def login_attempt(driver, username, password, frame):
    """Automatic Site Login.

    Args:
        driver (webdriver): selenium webdriver
    """
    # username = input("Enter 7cav.us Username(email):")
    # password = getpass.getpass(prompt="Enter 7cav.us Password:")
    """try:
        driver.find_element(
            "xpath",
            '//*[@id="top"]/div[2]/div[2]/div[2]/div\
                /nav/div/div[3]/div[1]/a[1]',
        )
    except NoSuchElementException:
        print("Retrying Login")
    else:
        confirm_login(driver)"""
    try:
        driver.find_element("xpath", '//*[@id="XF"]/body/div[2]/ul/li/div/div[2]/a[1]')
    except NoSuchElementException:
        pass
    else:
        ele_int("xpath", '//*[@id="XF"]/body/div[2]/ul/li/div/div[2]/a[1]', 1)
    driver.get("https://7cav.us/register/connected-accounts/keycloak/?setup=1")
    time.sleep(0.1)
    # input username
    ele_int("xpath", '//*[@id="username"]', 2, username)
    ele_int("xpath", '//*[@id="password"]', 2, password)
    ele_int("xpath", '//*[@id="kc-login"]', 1)
    try:
        driver.find_element("xpath", '//*[@id="kc-content-wrapper"]/div[1]')
    except NoSuchElementException:
        print("Logged in")
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
            twofa_screen()
    else:
        print("Invalid Username or Password Detected")
        wrong_pword = ctk.CTkLabel(master=frame, text="Invalid Username or Password")
        wrong_pword.pack(pady=12, padx=10)
        wrong_pword.after(7000, wrong_pword.destroy)


def two_fa(driver, twofa_code, frame):
    """Handle 2fa entry.

    Args:
        driver (webdriver): selected webdriver
    """
    # requests 2FA code from user and stores to variable
    # twofa_code = input("Enter 2FA Code:")
    # scroll to bottom of page to avoid click intercept
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # enters 2FA code into box
    ele_int("name", "code", 2, twofa_code)
    # clicks confirm button
    ele_int(
        "xpath",
        '//*[@id="top"]/div[2]/div[2]/div[6]/div/div/div[2]/div[2]/form/div\
            /dl/dd/div/div[2]/button',
        1,
    )
    time.sleep(1)
    try:
        driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[3]/div[2]/div[2]/div/nav/div/div[3]/div[1]/a[3]",
        )
    except NoSuchElementException:
        print("Incorrect 2FA Code")
        ele_int("xpath", '//*[@id="js-XFUniqueId2"]/div/div[1]/a', 1)
        wrong_twofa = ctk.CTkLabel(master=frame, text="Invalid 2FA Code")
        wrong_twofa.pack(pady=12, padx=10)
        wrong_twofa.after(7000, wrong_twofa.destroy)
    else:
        print("2FA Confirmed")
        entry_screen()


def milpac_create(
    driver,
    milpac_username,
    milpac_username_update,
    milpac_real_name,
    milpac_join_date,
    frame,
):
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
    # milpac_username = input("Enter current forum username:")
    # milpac_username_update = input("Update username to the following:")
    # milpac_real_name = input("Enter Real Name:")
    # milpac_join_date = input("Enter Join Date (YYYY-MM-DD):")
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
    return milpac_confirm(driver, frame)


def milpac_confirm(driver, frame):
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
        wrong_milpac = ctk.CTkLabel(master=frame, text="Invalid 2FA Code")
        wrong_milpac.pack(pady=12, padx=10)
        wrong_milpac.after(7000, wrong_milpac.destroy)
    else:
        print("Milpac Successfully Created")
        WebDriverWait(driver, timeout=10).until(
            ec.url_contains("https://7cav.us/rosters/profile/?unique_id=")
        )
        created_milpac = driver.current_url
        milpac_puc_add(driver, created_milpac)


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
        repeat_screen()


def login_button_event(uname_entry, pword_entry, frame):
    username = uname_entry.get()
    password = pword_entry.get()
    login_attempt(driver, username, password, frame)


def login_screen():
    clear_frame()
    frame = ctk.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = ctk.CTkLabel(master=frame, text="New Milpac Creation Automation")
    label.pack(pady=12, padx=10)

    label2 = ctk.CTkLabel(
        master=frame, text="Please Login using your 7cav.us credentials"
    )
    label2.pack(pady=12, padx=10)

    uname_entry = ctk.CTkEntry(master=frame, placeholder_text="Username")
    uname_entry.pack(pady=12, padx=10)

    pword_entry = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
    pword_entry.pack(pady=12, padx=10)

    button = ctk.CTkButton(
        master=frame,
        text="Login",
        command=lambda: login_button_event(uname_entry, pword_entry, frame),
    )
    button.pack(pady=12, padx=10)


def entry_screen():
    clear_frame()
    frame = ctk.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = ctk.CTkLabel(master=frame, text="New Milpac Creation Automation")
    label.pack(pady=12, padx=10)

    label2 = ctk.CTkLabel(
        master=frame, text="Please enter required information to create new milpac"
    )
    label2.pack(pady=12, padx=10)

    label3 = ctk.CTkLabel(master=frame, text="New Recruit's Current Forum Username")
    label3.pack(pady=12, padx=10)

    milpac_username_entry = ctk.CTkEntry(master=frame, placeholder_text="Old Username")
    milpac_username_entry.pack(pady=12, padx=10)

    label4 = ctk.CTkLabel(master=frame, text="New Recruit's New Forum Username")
    label4.pack(pady=12, padx=10)

    milpac_username_update_entry = ctk.CTkEntry(
        master=frame, placeholder_text="New Username"
    )
    milpac_username_update_entry.pack(pady=12, padx=10)

    label5 = ctk.CTkLabel(master=frame, text="New Recruit's Real Name")
    label5.pack(pady=12, padx=10)

    milpac_real_name_entry = ctk.CTkEntry(master=frame, placeholder_text="New Username")
    milpac_real_name_entry.pack(pady=12, padx=10)

    label6 = ctk.CTkLabel(master=frame, text="Join Date in format YYYY-MM-DD")
    label6.pack(pady=12, padx=10)

    milpac_join_date_entry = ctk.CTkEntry(master=frame, placeholder_text="YYYY-MM-DD")
    milpac_join_date_entry.pack(pady=12, padx=10)

    button = ctk.CTkButton(
        master=frame,
        text="Submit",
        command=lambda: milpac_button_event(
            milpac_username_entry,
            milpac_username_update_entry,
            milpac_real_name_entry,
            milpac_join_date_entry,
            frame,
        ),
    )
    button.pack(pady=12, padx=10)


def twofa_screen():
    clear_frame()
    frame = ctk.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = ctk.CTkLabel(master=frame, text="Two Factor Login Authentication")
    label.pack(pady=12, padx=10)

    label2 = ctk.CTkLabel(master=frame, text="Please enter your Two Factor Code")
    label2.pack(pady=12, padx=10)

    twofa_entry = ctk.CTkEntry(master=frame, placeholder_text="2FA Code")
    twofa_entry.pack(pady=12, padx=10)

    button = ctk.CTkButton(
        master=frame,
        text="Submit",
        command=lambda: twofa_button_event(twofa_entry, frame),
    )
    button.pack(pady=12, padx=10)


def repeat_screen():
    clear_frame()
    frame = ctk.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    repeat_label = ctk.CTkLabel(
        master=frame, text="Do you have any more entries to add?"
    )
    repeat_label.pack(pady=12, padx=10)

    repeat_button = ctk.CTkButton(master=frame, text="Yes", command=repeat_yes_button)
    repeat_button.pack(pady=12, padx=10)

    repeat_button_2 = ctk.CTkButton(master=frame, text="No", command=repeat_no_button)
    repeat_button_2.pack(pady=12, padx=10)


def repeat_yes_button():
    entry_screen()


def repeat_no_button():
    clear_frame()
    frame = ctk.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    exit_label = ctk.CTkLabel(
        master=frame,
        text="Thank you for using the Milpac Creation Automator by Sypolt.R",
    )
    exit_label.pack(pady=12, padx=10)

    exit_button = ctk.CTkButton(master=frame, text="Exit", command=exit)
    exit_button.pack(padx=12, pady=10)


def milpac_button_event(
    milpac_username_entry,
    milpac_username_update_entry,
    milpac_real_name_entry,
    milpac_join_date_entry,
    frame,
):
    milpac_username = milpac_username_entry.get()
    milpac_username_update = milpac_username_update_entry.get()
    milpac_real_name = milpac_real_name_entry.get()
    milpac_join_date = milpac_join_date_entry.get()
    return milpac_create(
        driver,
        milpac_username,
        milpac_username_update,
        milpac_real_name,
        milpac_join_date,
        frame,
    )


def twofa_button_event(twofa_entry, frame):
    twofa_code = twofa_entry.get()
    two_fa(driver, twofa_code, frame)


login_screen()
root.mainloop()

"""
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


# milpac_create(driver)
# created_milpac = milpac_confirm(driver)
# milpac_puc_add(driver, created_milpac)
"""
