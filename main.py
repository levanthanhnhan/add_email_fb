import os
from common import const
from controllers.change_email_controller import change_email
from controllers.save_cookies_controller import save_cookies
from models.account_model import Account

accounts = [
    Account(cookie="datr=IjNAY_6CNCmDovB9gtZrdeoO; sb=IjNAY62UzV2gmFoFVxEGmbGe; c_user=100017481168010; xs=38%3Ak2EHupQ6pfoPow%3A2%3A1665151885%3A-1%3A2520; m_page_voice=100017481168010; fr=0F8Py7w0tTqYFVZZF.AWXlzBj-Rz4iqYvcCINR3-O7aBM.BjQDMi.JL.AAA.0.0.Bja5bi.AWXo9b8M09U; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1667995369692%2C%22v%22%3A1%7D; wd=1365x961", username="lvtn_acc_01@outlook.com", password="admin@123456"),
    Account(cookie="datr=qDFAY8cQhPpCunvgT6b779Pj; sb=qDFAY9Yk6XOdF6iH2QrKuR7K; c_user=100050413003365; xs=48%3ATjyPab8mriKMPA%3A2%3A1665151479%3A-1%3A4718; m_page_voice=100050413003365; fr=0sJ2ndBJy7x5SpwPb.AWXZ5iMF4O83gvV4PQq4KRXAxXk.BjQDGo.Pn.AAA.0.0.Bja5ct.AWV7iP1b-jM; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1667995445739%2C%22v%22%3A1%7D; wd=1365x961; ", username="lvtn_acc_02@outlook.com", password="admin@123456"),
]

# change email
for account in accounts:
    # change email by account
    change_email(account)

    # remove access token file
    if os.path.exists(const.JSON_TOKEN_FILE_NAME):
        os.remove(const.JSON_TOKEN_FILE_NAME)
