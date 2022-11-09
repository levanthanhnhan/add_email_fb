import os
import json
import msal
import webbrowser
from common import const, login_state
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# define method login
use_login_state = login_state.LoginState.auto

# function get access token from application id register Azure Portal
def get_access_token(app_id, scopes, username, password):
    # save session token
    access_token_cache = msal.SerializableTokenCache()

    # assign a serializableTokenCache object to the client instance
    client = msal.PublicClientApplication(client_id=app_id, token_cache=access_token_cache)

    # read the token file
    if os.path.exists(const.JSON_TOKEN_FILE_NAME):
        access_token_cache.deserialize(open(const.JSON_TOKEN_FILE_NAME, "r").read())
        token_detail = json.load(open(const.JSON_TOKEN_FILE_NAME,))
        token_detail_key = list(token_detail['AccessToken'].keys())[0]
        token_expiration = datetime.fromtimestamp(int(token_detail['AccessToken'][token_detail_key]['expires_on']))
        if token_expired(token_expiration):
            # remove file
            os.remove(const.JSON_TOKEN_FILE_NAME)
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
            auto_login(flow['user_code'], username, password)
        else:
            # login step by step
            print('user_code: ' + flow['user_code'])
            webbrowser.open(const.LOGIN_DEVICE)

        token_response = client.acquire_token_by_device_flow(flow)

    with open(const.JSON_TOKEN_FILE_NAME, 'w') as _f:
        _f.write(access_token_cache.serialize())

    return token_response

# function check token is expired (true: expired)
def token_expired(token_expiration):
    return datetime.now() > token_expiration

# function auto login account
def auto_login(user_code, username, password):
    # define browser
    browser = webdriver.Chrome(executable_path="./chromedriver")
    browser.get(const.LOGIN_DEVICE)
    wait = WebDriverWait(browser, 60)

    # fill user_code
    txt_user_code = wait.until(EC.visibility_of_element_located((By.NAME, const.DOM_NAME_USER_CODE)))
    txt_user_code.send_keys(user_code)
    txt_user_code.send_keys(Keys.ENTER)

    # fill username
    txt_username = wait.until(EC.visibility_of_element_located((By.NAME, const.DOM_NAME_EMAIL)))
    txt_username.send_keys(username)
    txt_username.send_keys(Keys.ENTER)

    # fill password
    txt_password = wait.until(EC.visibility_of_element_located((By.NAME, const.DOM_NAME_PASSWORD)))
    txt_password.send_keys(password)
    txt_password.send_keys(Keys.ENTER)

    # submit form Stay Singed
    form_stay_signed = wait.until(EC.visibility_of_element_located((By.TAG_NAME, const.DOM_FORM_SUBMIT)))
    form_stay_signed.submit()

    # submit form permission
    btn_accpects = browser.find_elements(By.ID, const.DOM_FORM_ALLOW_PERMISSION)
    if len(btn_accpects) > 0:
        btn_accpects[0].send_keys(Keys.ENTER)
