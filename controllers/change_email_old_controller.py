from common import const
from time import sleep
from selenium import webdriver
from controllers.read_mail_controller import read_mail
from models.account_model import Account

# global code verify
code_verify = ''

#function add main and get code old version
def add_mail_and_get_code_old_fb(browser, account):
    global code_verify

    # handle old version (read js, execute)
    execute_js_old_fb(browser=browser, username=account.username)

    # reload page
    browser.get(const.URL_FACEBOOK_CHANGE_MAIL)

    # get code from email sent
    code_verify = read_mail(account.username, account.password, True)

# function execute js when is new version
def execute_js_old_fb(browser, username):
    # open file js
    with open("./execute_script.js") as file :
        filedata = file.read()
    
    # replace email
    filedata = filedata.replace('username_replace', username)

    # read js from file and excevute
    browser.execute_script(filedata)

    # sleep
    sleep(const.TIME_SLEEP)

# function fill code old version
def fill_code_old_fb(browser):
    global code_verify

    # click button confirm
    button_confirm = "document.getElementsByClassName('xh8yej3 xat3117 x1lliihq xxxdfa6 x112ta8 xwmqs3e x76ihet')[0].contentWindow.document.getElementsByClassName('SettingsEmailPendingConfirm')[0].click()"
    browser.execute_script(button_confirm)

    # sleep wait show dialog
    sleep(const.TIME_SLEEP)

    # fill code
    fill_code = "document.getElementsByClassName('xh8yej3 xat3117 x1lliihq xxxdfa6 x112ta8 xwmqs3e x76ihet')[0].contentWindow.document.getElementById('code').value='" + code_verify + "'"
    browser.execute_script(fill_code)

    # submit code
    submit_code = "document.getElementsByClassName('xh8yej3 xat3117 x1lliihq xxxdfa6 x112ta8 xwmqs3e x76ihet')[0].contentWindow.document.getElementsByTagName('form')[0].submit()"
    browser.execute_script(submit_code)

    # sleep
    sleep(const.TIME_SLEEP)

    # check submit status
    submit_err = "return document.getElementsByClassName('uiHeaderImage img sp_ot1t5YjYL3s sx_492c8e').length;" #uiHeaderImage img sp_ot1t5YjYL3s sx_492c8e class dialog show error
    submit_err_length = browser.execute_script(submit_err)
    if submit_err_length > 1:
        # ssave log err
        print()

    # sleep
    sleep(const.TIME_SLEEP)