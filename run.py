"""
Imported libraries to access and update data in 
e-vehicle-survey-data spreadsheet
"""
import gspread
from google.oauth2.service_account import Credentials

# The following code was taken from the love_sandwiches walkthrough project by CodeInstitute
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('e-vehicle-survey-data')

options = SHEET.worksheet('options')

data = options.get_all_values()

print(data)
