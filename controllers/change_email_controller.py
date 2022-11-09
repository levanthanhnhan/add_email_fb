import pickle
from common import const
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from controllers.read_mail_controller import read_mail
from services.cookies_service import parse_cookie

# region CHANGE EMAIL
# funtion change email
def change_email():
    # define browser
    browser = webdriver.Chrome(executable_path="./chromedriver")
    #browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.maximize_window()
    browser.get("http://facebook.com")

    # load cookies from file
    cookies = pickle.load(open("my_cookies.pkl", "rb"))

    # load cookies from raw data
    # raw_cookie_data = "datr=IjNAY_6CNCmDovB9gtZrdeoO; sb=IjNAY62UzV2gmFoFVxEGmbGe; c_user=100017481168010; xs=38%3Ak2EHupQ6pfoPow%3A2%3A1665151885%3A-1%3A2520; m_page_voice=100017481168010; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1667978739591%2C%22v%22%3A1%7D; fr=0F8Py7w0tTqYFVZZF.AWVLb2q0EQhlWRoLm8aGrWm2LMA.BjQDMi.JL.AAA.0.0.Bja1X8.AWV0JW99RzY; wd=1365x961"
    # cookies = parse_cookie(raw_cookie_data)

    # set cookies
    for cookie in cookies:
        browser.add_cookie(cookie)

    # reload page using cookies
    browser.get(const.URL_FACEBOOK_CHANGE_MAIL)

    # show contact point dialog and submit send code
    if is_new_facebook_version(browser):
        # handle new version (read js, execute)
        execute_js_new_version(browser=browser)

        # get code from email sent
        code_verify = read_mail()

        # fill code after get from mail
        fill_code_new(browser, code_verify)
    else:
        # handle old version (create a tag, open dialog)
        execute_js_old_version(browser=browser)

        # get code from email sent
        code_verify = read_mail()

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
        html_append = "var a_tag = document.createElement('a'); "
        html_append += "document.getElementsByClassName('xh8yej3 xat3117 x1lliihq xxxdfa6 x112ta8 xwmqs3e x76ihet')[0].contentWindow.document.getElementById('mainContainer').append(a_tag);"
        browser.execute_script(html_append)

        return False
    except:
        return True
# endregion

# region HANDLE NEW VERSION
# function execute js when is new version
def execute_js_new_version(browser):
    # read js from file and excevute
    browser.execute_script(open("./execute_script.js").read())

    # sleep
    sleep(const.TIME_SLEEP)

# function fill code new version
def fill_code_new(browser, code_verify):
    wait = WebDriverWait(browser, 60)

    # click button edit
    btnEdits = "document.getElementsByClassName('x1n2onr6 x1ja2u2z x78zum5 x2lah0s xl56j7k x6s0dn4 xozqiw3 x1q0g3np xi112ho x17zwfj4 x585lrc x1403ito x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xn6708d x1ye3gou x1qhmfi1 x1r1pt67')[1].click();"
    browser.execute_script(btnEdits)

    # click button confirm
    btnConfirm = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "x1n2onr6 x1ja2u2z x78zum5 x2lah0s xl56j7k x6s0dn4 xozqiw3 x1q0g3np xi112ho x17zwfj4 x585lrc x1403ito x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xn6708d x1ye3gou x1hr4nm9 x1r1pt67")))
    btnConfirm.click()

    # fill code
    txtCode = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "x1i10hfl xggy1nq x1s07b3s x1kdt53j x1a2a7pz xjbqb8w x76ihet xwmqs3e x112ta8 xxxdfa6 x9f619 xzsf02u x1uxerd5 x1fcty0u x132q4wb x1a8lsjc x1pi30zi x1swvt13 x9desvi xh8yej3 x15h3p50 x10emqs4")))
    txtCode.send_keys(code_verify)

    # submit code
    btnSubmit = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "x1n2onr6 x1ja2u2z x78zum5 x2lah0s xl56j7k x6s0dn4 xozqiw3 x1q0g3np xi112ho x17zwfj4 x585lrc x1403ito x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xn6708d x1ye3gou xtvsq51 x1r1pt67")))
    btnSubmit.click()
# endregion

# region HANDLE OLD VERSION
# function add element use click open dialog contact point when is old version
def execute_js_old_version(browser):
    wait = WebDriverWait(browser, 60)

    # add dialog
    html_append = "var a_tag = document.createElement('a'); "
    html_append += "a_tag.id='change_contactpoint_dialog'; "
    html_append += "a_tag.style.position='absolute'; a_tag.href = '/change_contactpoint/dialog/'; "
    html_append += "a_tag.innerText = 'Change Contactpoint Dialog'; a_tag.rel='dialog'; a_tag.role='button'; "
    html_append += "document.getElementsByClassName('xh8yej3 xat3117 x1lliihq xxxdfa6 x112ta8 xwmqs3e x76ihet')[0].contentWindow.document.getElementById('mainContainer').append(a_tag);"
    browser.execute_script(html_append)

    # sleep
    sleep(const.TIME_SLEEP)

    # show dialog
    show_dialog = "document.getElementsByClassName('xh8yej3 xat3117 x1lliihq xxxdfa6 x112ta8 xwmqs3e x76ihet')[0].contentWindow.document.getElementById('change_contactpoint_dialog').click();"
    browser.execute_script(show_dialog)

    # sleep
    sleep(const.TIME_SLEEP)

    # fill email
    fill_email = "document.getElementsByClassName('xh8yej3 xat3117 x1lliihq xxxdfa6 x112ta8 xwmqs3e x76ihet')[0].contentWindow.document.getElementsByName('contactpoint')[0].value='" + const.LOGIN_EMAIL + "'"
    browser.execute_script(fill_email)

    # submit email
    submit_email = "document.getElementsByClassName('xh8yej3 xat3117 x1lliihq xxxdfa6 x112ta8 xwmqs3e x76ihet')[0].contentWindow.document.getElementsByTagName('form')[0].submit()"
    browser.execute_script(submit_email)

    # reload page using cookies
    browser.get(const.URL_FACEBOOK_CHANGE_MAIL)

# function fill code old version
def fill_code_old(browser, code_verify):
    # click button confirm
    button_confirm = "document.getElementsByClassName('xh8yej3 xat3117 x1lliihq xxxdfa6 x112ta8 xwmqs3e x76ihet')[0].contentWindow.document.getElementsByClassName('SettingsEmailPendingConfirm')[0].click()"
    browser.execute_script(button_confirm)

    # sleep
    sleep(const.TIME_SLEEP)

    # fill code
    fill_code = "document.getElementsByClassName('xh8yej3 xat3117 x1lliihq xxxdfa6 x112ta8 xwmqs3e x76ihet')[0].contentWindow.document.getElementById('code').value='" + code_verify + "'"
    browser.execute_script(fill_code)

    # submit code
    submit_code = "document.getElementsByClassName('xh8yej3 xat3117 x1lliihq xxxdfa6 x112ta8 xwmqs3e x76ihet')[0].contentWindow.document.getElementsByTagName('form')[0].submit()"
    browser.execute_script(submit_code)
# endregion