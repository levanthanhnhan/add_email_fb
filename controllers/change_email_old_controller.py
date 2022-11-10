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

    # handle new version (read js, execute)
    execute_js_old_fb(browser=browser, username=account.username)

    # get code from email sent
    code_verify = read_mail(account.username, account.password)

# function add element use click open dialog contact point when is old version
def execute_js_old_fb(browser, username):
    # add dialog
    html_append =  "var a_tag = document.createElement('a'); "
    html_append += "a_tag.id='change_contactpoint_dialog'; "
    html_append += "a_tag.style.position='absolute'; a_tag.href = '/change_contactpoint/dialog/'; "
    html_append += "a_tag.innerText = 'Change Contact Point Dialog'; a_tag.rel='dialog'; a_tag.role='button'; "
    html_append += "document.getElementsByClassName('xh8yej3 xat3117 x1lliihq xxxdfa6 x112ta8 xwmqs3e x76ihet')[0].contentWindow.document.getElementById('mainContainer').append(a_tag);"
    browser.execute_script(html_append)

    # sleep wait show dialog
    sleep(const.TIME_SLEEP)

    # show dialog
    show_dialog = "document.getElementsByClassName('xh8yej3 xat3117 x1lliihq xxxdfa6 x112ta8 xwmqs3e x76ihet')[0].contentWindow.document.getElementById('change_contactpoint_dialog').click();"
    browser.execute_script(show_dialog)

    # sleep wait show dialog
    sleep(const.TIME_SLEEP)

    # fill email
    fill_email = "document.getElementsByClassName('xh8yej3 xat3117 x1lliihq xxxdfa6 x112ta8 xwmqs3e x76ihet')[0].contentWindow.document.getElementsByName('contactpoint')[0].value='" + username + "'"
    browser.execute_script(fill_email)

    # sleep wait show dialog
    sleep(const.TIME_SLEEP)

    # submit email
    submit_email = "document.getElementsByClassName('xh8yej3 xat3117 x1lliihq xxxdfa6 x112ta8 xwmqs3e x76ihet')[0].contentWindow.document.getElementsByTagName('form')[0].submit()"
    browser.execute_script(submit_email)

    # reload page when add mail success
    browser.get(const.URL_FACEBOOK_CHANGE_MAIL)

# function fill code old version
def fill_code_old_fb(browser, handleError=None):
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
    if (submit_err_length > 1) & (handleError != None):
        new_account = Account("", "", "")
        handleError(browser, new_account)

    # sleep
    sleep(const.TIME_SLEEP)