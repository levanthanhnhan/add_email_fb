import requests
from time import sleep
from common import const
from controllers.auth_controller import get_access_token
from services.email_service import parse_email_from_api

# defined count repeat get mail
repeat_get_mail_count = 0

def read_mail(username, password, isVerify):
    # mark global
    global repeat_get_mail_count
    
    # increment count
    repeat_get_mail_count += 1

    # send request get email
    code_verify_new = request_get_email(username, password, isVerify)

    # if account never recived code from facebook
    if code_verify_new == "":
        while repeat_get_mail_count < const.REPEAT_GET_MAIL_COUNT:
            # sleep 10s to recall
            sleep(10)
            # re-get mail
            read_mail(username=username, password=password)
    
    return code_verify_new

# function send request get email
def request_get_email(username, password, isVerify):
    code_verify = ""

    #get access token by application (client) id and scopes permission
    access_token = get_access_token(const.APP_ID, const.SCOPES, username, password)

    # add access token to header
    headers = {
        'Authorization': 'Bearer ' + access_token['access_token'],
        'Prefer': 'outlook.body-content-type="text"'
    }

    # define Endpoint
    endpoint = const.GRAPH_API_ENDPOINT + const.GET_EMAIL_BY_FILTER

    # send request with endpoint and header using Bearer token
    response = requests.get(endpoint, headers=headers)

    # get response
    if response.status_code == 200:
        emails = parse_email_from_api(response.text)
        for email in emails:
            print("<!------ GET EMAIL SUCCESS ------!>")

            # get code
            code = get_code(email.body, isVerify)
            if code.isnumeric():
                code_verify = code
                break
    else:
        print(response.reason)

    return code_verify

# function get code from body email
def get_code(body, isVerify):
    if isVerify:
        contents_1 = body.split('https://www.facebook.com/confirmcontact.php?c=')
        contents_2 = contents_1[1].split('&')
        code = contents_2[0]
        return code
    else:
        contents_1 = body.split('https://www.facebook.com/recover/code/?n=')
        contents_2 = contents_1[1].split('&')
        code = contents_2[0]
        return code
