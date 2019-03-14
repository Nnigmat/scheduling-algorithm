import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('Trygoogle-50a92384d71a.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open('Answers').sheet1
print(wks.get_all_records())
# print(dir(wks))
