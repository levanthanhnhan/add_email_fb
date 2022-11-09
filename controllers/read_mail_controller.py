import requests
from common import const
from services.auth_service import get_access_token
from services.email_service import parse_email_from_api

def read_mail(username, password):
    # defined code verify
    code_verify = ''

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
            print("<!------ BEGIN EMAIL ------!>")
            print("Email Id: " + email.id)
            print("Email Body: " + email.body)
            print("<!------- END EMAIL -------!>")

            # get code
            _code = get_code(email.body)
            if _code.isnumeric():
                code_verify = _code
                break
    else:
        print(response.reason)

    return code_verify

# function get code from body email
def get_code(body):
    contents = body.split(const.SPLIT_CODE_CHARACTER)
    code = contents[1][0:5]
    return code
