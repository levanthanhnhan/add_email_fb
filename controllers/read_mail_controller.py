import requests
from time import sleep
from common import const
from services.auth_service import get_access_token
from services.email_service import parse_email_from_api
from models.respone_email import ResponseEmail

# defined count repeat get mail
repeat_get_mail_count = 0

def read_mail(username, password):
    # mark global
    global repeat_get_mail_count
    
    # increment count
    repeat_get_mail_count += 1

    # send request get email
    response_email_new = request_get_email(username, password)

    # if account never recived code from facebook
    if response_email_new.id == "":
        while repeat_get_mail_count < const.REPEAT_GET_MAIL_COUNT:
            # sleep 10s to recall
            # sleep(10)
            # re-get mail
            read_mail(username=username, password=password)
    
    return response_email_new.code

# function send request get email
def request_get_email(username, password):
    response_email = ResponseEmail(id="", code="")

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
            code = get_code(email.body)
            if code.isnumeric():
                response_email.id = email.id
                response_email.code = code
                break
    else:
        print(response.reason)

    return response_email

# function get code from body email
def get_code(body):
    contents = body.split(const.SPLIT_CODE_CHARACTER)
    code = contents[1][0:5]
    return code
