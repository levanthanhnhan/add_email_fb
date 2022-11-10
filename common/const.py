# app_id register from Azure Portal (https://portal.azure.com/)
APP_ID = '76bb323e-238f-454d-b613-3d3d8209d4bb'

# scopes use permission app
SCOPES = ['Mail.Read']

# endpoint api graph microsoft
GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'

# request URL: login device
LOGIN_DEVICE = 'https://microsoft.com/devicelogin'

# request URL: get all messages (email) by filter:
# $search from: get email by from value.
# $select: select properties email. (not set: select all)
# $top: select limit records. (not set: default 10 records)
GET_EMAIL_BY_FILTER = '/me/messages?$search="from:security1234@facebookmail.com"&$select=id,subject,body,from&$top=1000'

# time sleep when fill value
TIME_SLEEP = 5

# DOM element by name write user_code
DOM_NAME_USER_CODE = 'otc'

# DOM element by name write email
DOM_NAME_EMAIL = 'loginfmt'

# DOM element by name write password
DOM_NAME_PASSWORD = 'passwd'

# DOM element form confirm login stayed
DOM_FORM_SUBMIT = 'form'

# DOM element form allow permission
DOM_FORM_ALLOW_PERMISSION = 'idBtn_Accept'

# split code character from email
SPLIT_CODE_CHARACTER = ': '

# URL change email
URL_FACEBOOK_CHANGE_MAIL = 'https://www.facebook.com/settings?tab=account&section=email'

# json stored token file name
JSON_TOKEN_FILE_NAME = 'ms_graph_api_token.json'

# repeat send get mail count
REPEAT_GET_MAIL_COUNT = 2
