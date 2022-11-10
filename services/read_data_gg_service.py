import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
from models.account_model import Account

scope = ['https://www.googleapis.com/auth/drive']        
creds = ServiceAccountCredentials.from_json_keyfile_name('token.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1NDfSBR_15D4zKzneVJIxAhJ1cfsWEvFbGnYzePgsHAQ')
sheet_Cookies = sheet.worksheet('Cookies')       
cookies = sheet_Cookies.get_all_records()

# Get cookies
lstCookies = []

def get_cookies_google_sheet():
    for i, item in enumerate(cookies, start=0):
        new_output = list(cookies[i].values())
        cookie = new_output[0]
        newPassword = new_output[1] 
        fa2 = new_output[2] 
        email = new_output[3]
        hotmai_username =  email.split("|")[0]
        hotmai_password =  email.split("|")[1]
        dateChange = new_output[4] 
        sttCookie = new_output[5]
        account = Account(cookie=cookie, username=hotmai_username, password=hotmai_password, newPassword=newPassword, status=sttCookie)
        lstCookies.append(account)

    return lstCookies

def change_status_success_google_sheet(idx):
    today = date.today()
    dateChange = today.strftime("%d/%m/%Y")
    sheet_Cookies.update('E'+str(idx+2), dateChange) 
    sheet_Cookies.update('F'+str(idx+2), "OK")