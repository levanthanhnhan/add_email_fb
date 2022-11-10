from common import const
from time import sleep
from selenium import webdriver
from controllers.read_mail_controller import read_mail
from controllers.change_password_controller import change_password
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

    # load cookies from raw data
    cookies = parse_cookie(account.cookie)

    # set cookies
    for cookie in cookies:
        browser.add_cookie(cookie)

    # reload page using cookies
    browser.get(const.URL_FACEBOOK_CHANGE_MAIL)

    # check checkpoint
    if check_point(browser=browser): False

    # handle with fb version
    if is_new_facebook_version(browser):
        # add mail and get code
        add_mail_and_get_code_new_fb(browser=browser, account=account)

        # fill code after get from mail
        fill_code_new_fb(browser)
    else:
        # add mail and get code
        add_mail_and_get_code_old_fb(browser=browser, account=account)

        # fill code after get from mail
        fill_code_old_fb(browser)

    # reload page success
    browser.get(const.URL_FACEBOOK_CHANGE_MAIL)

    # sleep
    sleep(const.TIME_SLEEP)
    
    # change password
    change_password(browser, account)

    # check checkpoint
    if check_point(browser=browser): False

    return True

# function detect facebook version (true: new, false: old)
def is_new_facebook_version(browser):
    try:
        # sleep
        sleep(const.TIME_SLEEP)

        # detect
        html_append =  "var a_tag = document.createElement('a'); "
        html_append += "document.getElementsByClassName('xh8yej3 xat3117 x1lliihq xxxdfa6 x112ta8 xwmqs3e x76ihet')[0].contentWindow.document.getElementById('mainContainer').append(a_tag);"
        browser.execute_script(html_append)

        return False
    except:
        return True

def check_point(browser):
    url_checkpoint = browser.current_url
    if "checkpoint" in url_checkpoint:
        print("Check point")
        return False

    return True