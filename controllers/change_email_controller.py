from common import const
from time import sleep
from selenium import webdriver
from controllers.read_mail_controller import read_mail
from services.cookies_service import parse_cookie
from models.account_model import Account

# global code verify
code_verify = ''

# region CHANGE EMAIL
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
        fill_code_new(browser, add_mail_and_get_code_new_fb)
    else:
        # handle old version (create a tag, open dialog)
        execute_js_old_version(browser=browser, username=account.username)

        # get code from email sent
        code_verify = read_mail(account.username, account.password)

        # fill code after get from mail
        fill_code_old(browser, code_verify)

    # reload page success
    browser.get(const.URL_FACEBOOK_CHANGE_MAIL)
    
    sleep(5000)
# endregion

# region DETECT FACEBOOK VERSION
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
# endregion

# region HANDLE NEW VERSION
#function add main and get code new version
def add_mail_and_get_code_new_fb(browser, account):
    global code_verify

    # handle new version (read js, execute)
    execute_js_new_version(browser=browser, username=account.username)

    # get code from email sent
    code_verify = read_mail(account.username, account.password)

# function execute js when is new version
def execute_js_new_version(browser, username):
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
def fill_code_new(browser, handleError=None):
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
# endregion

# region HANDLE OLD VERSION
# function add element use click open dialog contact point when is old version
def execute_js_old_version(browser, username):
    # add dialog
    html_append =  "var a_tag = document.createElement('a'); "
    html_append += "a_tag.id='change_contactpoint_dialog'; "
    html_append += "a_tag.style.position='absolute'; a_tag.href = '/change_contactpoint/dialog/'; "
    html_append += "a_tag.innerText = 'Change Contactpoint Dialog'; a_tag.rel='dialog'; a_tag.role='button'; "
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
def fill_code_old(browser, handleError=None):
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
    submit_err = "return document.getElementsByClassName('uiOverlayFooter').length;" #uiOverlayFooter class dialog show error
    submit_err_length = browser.execute_script(submit_err)
    if (submit_err_length > 1) & (handleError != None):
        new_account = Account("", "", "")
        handleError(browser, new_account)
# endregion