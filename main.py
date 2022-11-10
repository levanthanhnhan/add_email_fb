import os
from common import const
from controllers.change_email_controller import change_email
from models.account_model import Account

accounts = [
    Account(cookie="sb=1aZsY4bPWLRFGJO1IJWhO7Q7; wd=1366x657; datr=1aZsYyzk6JSWSBghEk7zzjN5; c_user=100037946119603; xs=40%3A0QbiTJV_bKBD3Q%3A2%3A1668064993%3A-1%3A7346%3A%3AAcUiQhbr8Hli6u9Z_tHBmzaO8dzRUWy1FuYiD0tNsw; fr=0Hvf1dCOiRMhT3xGa.AWX3ikVjC7NRMeN3-hL7f9TZth4.BjbMMd.cZ.AAA.0.0.BjbMMd.AWVscoQF8do; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1668072225675%2C%22v%22%3A1%7D", username="lvtn_acc_03@outlook.com", password="admin@123456"),
    #Account(cookie="datr=IjNAY_6CNCmDovB9gtZrdeoO; sb=IjNAY62UzV2gmFoFVxEGmbGe; c_user=100017481168010; xs=38%3Ak2EHupQ6pfoPow%3A2%3A1665151885%3A-1%3A2520; m_page_voice=100017481168010; fr=0F8Py7w0tTqYFVZZF.AWXlzBj-Rz4iqYvcCINR3-O7aBM.BjQDMi.JL.AAA.0.0.Bja5bi.AWXo9b8M09U; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1667995369692%2C%22v%22%3A1%7D; wd=1365x961", username="lvtn_acc_02@outlook.com", password="admin@123456"),
    #Account(cookie="datr=qDFAY8cQhPpCunvgT6b779Pj; sb=qDFAY9Yk6XOdF6iH2QrKuR7K; c_user=100050413003365; xs=48%3ATjyPab8mriKMPA%3A2%3A1665151479%3A-1%3A4718; m_page_voice=100050413003365; fr=0sJ2ndBJy7x5SpwPb.AWXZ5iMF4O83gvV4PQq4KRXAxXk.BjQDGo.Pn.AAA.0.0.Bja5ct.AWV7iP1b-jM; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1667995445739%2C%22v%22%3A1%7D; wd=1365x961; ", username="lvtn_acc_02@outlook.com", password="admin@123456"),
]

for account in accounts:
    # change email by account
    change_email(account)

    # remove access token file
    if os.path.exists(const.JSON_TOKEN_FILE_NAME):
        os.remove(const.JSON_TOKEN_FILE_NAME)
