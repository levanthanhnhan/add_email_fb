import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def save_cookies():
    # define browser
    browser = webdriver.Chrome(executable_path="./chromedriver")
    browser.maximize_window()
    browser.get("http://facebook.com")
    wait = WebDriverWait(browser, 60)

    # fill email
    txtEmail = wait.until(EC.visibility_of_element_located((By.ID, "email")))
    txtEmail.send_keys("fb_email")

    # fill password
    txtPassword = wait.until(EC.visibility_of_element_located((By.ID, "pass")))
    txtPassword.send_keys("fb_password")
    txtPassword.send_keys(Keys.ENTER)

    # save cookies to file
    pickle.dump(browser.get_cookies(), open("my_cookies.pkl", "wb"))

    # close browser
    browser.close()