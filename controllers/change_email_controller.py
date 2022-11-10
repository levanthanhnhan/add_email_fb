from common import const
from time import sleep
from selenium import webdriver
from controllers.read_mail_controller import read_mail
from controllers.change_email_new_controller import add_mail_and_get_code_new_fb, fill_code_new_fb
from controllers.change_email_old_controller import add_mail_and_get_code_old_fb, fill_code_old_fb
from services.cookies_service import parse_cookie
from models.account_model import Account

# funtion change email
def change_email(account):
    # define browser
    browser = webdriver.Chrome(executable_path="./chromedriver")
    browser.maximize_window()
    browser.get("https://www.facebook.com/")

    # load cookies from file
    # cookies = pickle.load(open("my_cookies.pkl", "rb"))

    # load cookies from raw data
    cookies = parse_cookie(account.cookie)

    # set cookies
    for cookie in cookies:
        browser.add_cookie(cookie)

    # reload page using cookies
    browser.get(const.URL_FACEBOOK_CHANGE_MAIL)

    # handle with fb version
    if is_new_facebook_version(browser):
        # add mail and get code
        add_mail_and_get_code_new_fb(browser=browser, account=account)

        # fill code after get from mail
        fill_code_new_fb(browser, add_mail_and_get_code_new_fb)
    else:
        # add mail and get code
        add_mail_and_get_code_old_fb(browser=browser, account=account)

        # fill code after get from mail
        fill_code_old_fb(browser, add_mail_and_get_code_new_fb)

    # reload page success
    browser.get(const.URL_FACEBOOK_CHANGE_MAIL)
    
    sleep(5000)

# function detect facebook version (true: new, false: old)
def is_new_facebook_version(browser):
    try:
        # sleep
        sleep(const.TIME_SLEEP)

        html_append =  "var a_tag = document.createElement('a'); "
        html_append += "document.getElementsByClassName('xh8yej3 xat3117 x1lliihq xxxdfa6 x112ta8 xwmqs3e x76ihet')[0].contentWindow.document.getElementById('mainContainer').append(a_tag);"
        browser.execute_script(html_append)

        return False
    except:
        return True