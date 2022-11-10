from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from controllers.read_mail_controller import read_mail
from models.account_model import Account

def change_password(browser, account):
    wait = WebDriverWait(browser, 5)
    browser.get("https://www.facebook.com/recover/initiate/")

    while True:
        btnContinue = browser.find_elements(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div/div[1]/div/div/div/div/div[6]/div/div[2]/div/div[2]/div[1]/div/div[1]/div/span/span')
        if len(btnContinue) > 0:
            btnContinue[0].click()
            sleep(1)
        else: break

    sleep(5)

    code_forget_passs = read_mail(account.username, account.password, False)

    txtFillCode = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div/div[1]/div/div/div[2]/div[2]/div[1]/div/label/div/div/input')))
    txtFillCode.send_keys(code_forget_passs)

    btnContinueForget = browser.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div/div[1]/div/div/div[3]/div[2]/div[2]/div[1]/div/div[1]/div/span/span')
    btnContinueForget.click()

    txtFillNewPassword = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div/div[1]/div/div/div/div/div[4]/div/div/div[3]/div/div[1]/div/div/label/div/div[1]/input')))
    txtFillNewPassword.send_keys(account.newPassword)

    btnContinueNewPassword = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div/div[1]/div/div/div/div/div[6]/div/div[2]/div[1]/div/div[1]/div/span/span')))
    btnContinueNewPassword.click()