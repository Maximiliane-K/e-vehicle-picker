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

def intro():
    """
    Introduction to the app
    """
    print("Welcome to Electric Vehicle Picker!\n")
    print(("This app is meant to support you and your customer on the journey"
        " of finding the right match when it comes to a new e-vehicle.\n"))
    print(("Follow the instructions given to get an recommendation and save"
        " the the data for further analysis."))

intro()
