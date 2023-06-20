"""
Imported libraries to access and update data in 
e-vehicle-survey-data spreadsheet
"""
import gspread
from google.oauth2.service_account import Credentials

# The following code was taken from the love_sandwiches 
# walkthrough project by CodeInstitute
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
    print(("Follow the instructions given to get a recommendation and save"
           " the customer data for further analysis.\n"))


def get_customer_details():
    """
    Get the customers' full name, age, gender
    and the info if they already drive electric.
    """
    print(("Please enter the 4 customer details as discribed below"
           "sepperated by a comma without spaces."))
    details = ["1. Full Name: enter customers first name and surname", 
               "2. Age: enter customers' age",
               "3. Gender: enter m,f or d",
               "4. Already drive electric? : enter yes or no\n"]
    print(*details, sep = "\n\n")
    print("Example: June Austin,35,f,no\n")

    details_str = input("Enter customer details here: ")

    customer_details = details_str.split(",")

    return customer_details


def update_customer_details_worksheet(details):
    """
    Update customers worksheet, add new row with customer details
    """
    print("Updating customers worksheet...\n")
    customers_worksheet = SHEET.worksheet("customers")
    customers_worksheet.append_row(customer_details)
    print("Customer details successfully added to customers worksheet.\n")

def select_car_type():
    """
    Function provides a selection of types of cars to the user 
    to be able to get an user input. 
    Run a while loop to repeatedly request data, until user input is valid.
    """
    while True:
        print("Please choose the preffered style of car.\n")
        styles = ["a) Microcar", "b) Compact Car", "c) Hatchback", "d) SUV", "e) Sedan", "f) Cabrio\n"]
        print(*styles, sep = "\n")

        type_choices = input("Only select one letter [a, b, c, d, e, f]: \n")

        customer_choice = type_choices.lower().strip()
        print("Validating entered value...\n")

        if validate_style_choice(customer_choice):
            print(f"Entry '{customer_choice}' is valid. Processing data...\n")
            break

    return customer_choice


def validate_style_choice(customer_choice):
    """
    Function to validate if the user input given is valid.
    """
    try:
        if customer_choice not in ["a", "b", "c", "d", "e", "f"]:
            raise ValueError(
                f"You entered '{customer_choice}'. \nOnly letters from a-f are valid"
            )
    except ValueError as e:
        print(f"Entry not valid:\n{e}, please try again.\n")
        return False

    return True
    

intro()
details = get_customer_details()
customer_details = [detail for detail in details]
update_customer_details_worksheet(customer_details)
select_car_type()

