import os
import json
import msal
import webbrowser
from common import const, login_state
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# define method login
use_login_state = login_state.LoginState.auto

# function get access token from application id register Azure Portal
def get_access_token(app_id, scopes):
    # save session token
    access_token_cache = msal.SerializableTokenCache()

    # assign a serializableTokenCache object to the client instance
    client = msal.PublicClientApplication(client_id=app_id, token_cache=access_token_cache)

    # read the token file
    if os.path.exists('ms_graph_api_token.json'):
        access_token_cache.deserialize(open("ms_graph_api_token.json", "r").read())
        token_detail = json.load(open('ms_graph_api_token.json',))
        token_detail_key = list(token_detail['AccessToken'].keys())[0]
        token_expiration = datetime.fromtimestamp(int(token_detail['AccessToken'][token_detail_key]['expires_on']))
        if token_expired(token_expiration):
            # remove file
            os.remove('ms_graph_api_token.json')
            access_token_cache = msal.SerializableTokenCache()

            # call api refresh token
            refresh_token_key = list(token_detail['RefreshToken'].keys())[0]
            refresh_token_secret = token_detail['RefreshToken'][refresh_token_key]['secret']
            client.acquire_token_by_refresh_token(refresh_token=refresh_token_secret, scopes=scopes)

    accounts = client.get_accounts()
    if accounts:
        # load the session
        token_response = client.acquire_token_silent(scopes, accounts[0])
    else:
        # authentication account
        flow = client.initiate_device_flow(scopes=scopes)

        # using method login
        if use_login_state == login_state.LoginState.auto:
            # login auto
            auto_login(flow['user_code'])
        else:
            # login step by step
            print('user_code: ' + flow['user_code'])
            webbrowser.open('https://microsoft.com/devicelogin')

        token_response = client.acquire_token_by_device_flow(flow)

    with open('ms_graph_api_token.json', 'w') as _f:
        _f.write(access_token_cache.serialize())

    return token_response

# function check token is expired (true: expired)
def token_expired(token_expiration):
    return datetime.now() > token_expiration

# function auto login account
def auto_login(user_code):
    # define browser
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(const.LOGIN_DEVICE)
    wait = WebDriverWait(browser, 60)

    # fill user_code
    txtUserCode = wait.until(EC.visibility_of_element_located((By.NAME, const.DOM_NAME_USER_CODE)))
    txtUserCode.send_keys(user_code)
    txtUserCode.send_keys(Keys.ENTER)

    # fill email
    txtEmail = wait.until(EC.visibility_of_element_located((By.NAME, const.DOM_NAME_EMAIL)))
    txtEmail.send_keys(const.LOGIN_EMAIL)
    txtEmail.send_keys(Keys.ENTER)

    # fill password
    txtPass = wait.until(EC.visibility_of_element_located((By.NAME, const.DOM_NAME_PASSWORD)))
    txtPass.send_keys(const.LOGIN_PASSWORD)
    txtPass.send_keys(Keys.ENTER)

    # submit form Stay Singed
    formStaySigned = wait.until(EC.visibility_of_element_located((By.TAG_NAME, const.DOM_FORM_SUBMIT)))
    formStaySigned.submit()

    # submit form permission
    btnAccpects = browser.find_elements(By.ID, const.DOM_FORM_ALLOW_PERMISSION)
    if len(btnAccpects) > 0:
        btnAccpects[0].send_keys(Keys.ENTER)
