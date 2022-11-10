from common import const
from time import sleep
from selenium import webdriver
from controllers.read_mail_controller import read_mail
from services.cookies_service import parse_cookie
from models.account_model import Account

# global code verify
code_verify = ''

#function add main and get code new version
def add_mail_and_get_code_new_fb(browser, account):
    global code_verify

    # handle new version (read js, execute)
    execute_js_new_fb(browser=browser, username=account.username)

    # get code from email sent
    code_verify = read_mail(account.username, account.password)

# function execute js when is new version
def execute_js_new_fb(browser, username):
    # open file js
    with open("./execute_script.js") as file :
        filedata = file.read()
    
    # replace email
    filedata = filedata.replace('username_replace', username)

    # read js from file and excevute
    browser.execute_script(filedata)

    # sleep
    sleep(const.TIME_SLEEP)

# function fill code new version
def fill_code_new_fb(browser, handleError=None):
    global code_verify

    # click button edit
    btn_edits = "document.getElementsByClassName('x1n2onr6 x1ja2u2z x78zum5 x2lah0s xl56j7k x6s0dn4 xozqiw3 x1q0g3np xi112ho x17zwfj4 x585lrc x1403ito x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xn6708d x1ye3gou x1qhmfi1 x1r1pt67')[1].click();"
    browser.execute_script(btn_edits)

    # click button confirm
    btn_confirm = "document.getElementsByClassName('x1n2onr6 x1ja2u2z x78zum5 x2lah0s xl56j7k x6s0dn4 xozqiw3 x1q0g3np xi112ho x17zwfj4 x585lrc x1403ito x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xn6708d x1ye3gou x1hr4nm9 x1r1pt67')[0].click();"
    browser.execute_script(btn_confirm)

    # sleep wait show modal
    sleep(const.TIME_SLEEP)

    # create custom input addpend to footer modal
    txt_input_custom =  "var button_custom = document.createElement('button'); "
    txt_input_custom += "button_custom.id='button_custom_focus_code'; "
    txt_input_custom += "button_custom.innerText ='Focus'; "
    txt_input_custom += "button_custom.onclick = function(){document.getElementById('jsc_c_13').focus();};"
    txt_input_custom += "document.getElementsByClassName('x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x13a6bvl x1qjc9v5 xozqiw3 x1q0g3np xn6708d x1ye3gou xyamay9 xcud41i x139jcc6 x4vbgl9 x1rdy4ex')[0].append(button_custom);"
    browser.execute_script(txt_input_custom)

    # focus input code
    txt_input_focus = browser.find_element("id", "button_custom_focus_code")
    txt_input_focus.click()

    # fill code
    txt_fill_code = "document.getElementsByClassName('x1i10hfl xggy1nq x1s07b3s x1kdt53j x1a2a7pz xjbqb8w x76ihet xwmqs3e x112ta8 xxxdfa6 x9f619 xzsf02u x1uxerd5 x1fcty0u x132q4wb x1a8lsjc x1pi30zi x1swvt13 x9desvi xh8yej3 x15h3p50 x10emqs4')[0].value='" + code_verify + "';"
    browser.execute_script(txt_fill_code)

    # submit code
    btn_submit = "document.getElementsByClassName('x1n2onr6 x1ja2u2z x78zum5 x2lah0s xl56j7k x6s0dn4 xozqiw3 x1q0g3np xi112ho x17zwfj4 x585lrc x1403ito x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xn6708d x1ye3gou xtvsq51 x1r1pt67')[0].click();"
    browser.execute_script(btn_submit)

    # sleep wait show modal
    sleep(const.TIME_SLEEP)

    # check submit status
    submit_err = "return document.getElementsByClassName('x1b0d499 x1d2xfc3').length;" #x1b0d499 x1d2xfc3 is icon error when show
    submit_err_length = browser.execute_script(submit_err)
    if (submit_err_length > 0) & (handleError != None):
        new_account = Account("", "", "")
        handleError(browser, new_account)

    # sleep
    sleep(const.TIME_SLEEP)