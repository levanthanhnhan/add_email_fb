import os
from common import const
from controllers.change_email_controller import change_email
from services.read_data_gg_service import get_cookies_google_sheet, change_status_success_google_sheet

accounts = get_cookies_google_sheet()

for idx, account in enumerate(accounts, start=0):
    try:
        # check status success
        if account.status == "OK":
            continue

        # change email by account
        res = change_email(account)
        if res == False:
            continue

        # change status success gg sheet
        change_status_success_google_sheet(idx)

        # remove access token file
        if os.path.exists(const.JSON_TOKEN_FILE_NAME):
            os.remove(const.JSON_TOKEN_FILE_NAME)
    except Exception as e:
        print(e)
        continue

