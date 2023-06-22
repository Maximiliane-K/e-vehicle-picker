"""
Imported libraries to access and update data in 
e-vehicle-survey-data spreadsheet
"""
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
    print(("This app is meant to support you and your customer to find"
           " the right match when it comes to a new e-vehicle.\n"))
    print(("Follow the instructions given to get a recommendation and save"
           " the customer data for further analysis.\n"))


def get_customer_details():
    """
    Get the customers' full name, age, gender
    and the info if they already drive electric.
    """
    while True:
        print(("Please enter the 4 customer details as discribed below\n" \
               "sepperated by a comma without spaces:\n"))
        details = ["1. Full Name: enter customers first name and surname", 
                   "2. Age: enter customers' age",
                   "3. Gender: enter m,f or d",
                   "4. Already drive electric? : enter yes or no\n"]

        print(*details, sep="\n\n")
        print("Example: June Austin, 35, f, no\n")

        details_str = input("Enter customer details here: ")

        customer_details = details_str.split(",")

        if validate_data_input(customer_details):
            print("Data valid!")
            break

    return customer_details


def validate_data_input(customer_details):
    """
    Function to validate if the customer details given 
    are valid.
    """
    try:
        # code from CodeInstitute love_sandwiches walkthrough project
        # check if the length of input is valid
        if len(customer_details) != 4:
            raise ValueError(
                f"Exactly 4 values are required"
            )

        # check for empty input
        if customer_details == "":
            raise ValueError(
                f"You didn't enter any value: {len(customer_details)}"
            )

        # check if full name value is numeric
        if customer_details[0].isnumeric():
            raise ValueError(
                f"You entered {customer_details[0]} as first value."\
                " First value has to be full name"
            )

        # check if full name value is empty
        if customer_details[0] == "":
            raise ValueError(
                f"You did not enter the full name"
            )
        
        # check if age value is empty
        if customer_details[1] == "":
            raise ValueError(
                f"You did not enter the age"
            )

        # check if age value is alphabetic
        if customer_details[1].isalpha():
            raise ValueError(
                f"You entered {customer_details[1]} as second value."\
                " Second value has to be a number"
            )
        
        # check if gender value is empty
        if customer_details[2] == "":
            raise ValueError(
                f"You did not enter the gender"
            )
        
        # check if gender value is numeric
        if customer_details[2].isnumeric():
            raise ValueError(
                f"You entered {customer_details[2]} as third value."\
                " Third value has to be m,f or d for gender"
            )
        
        # check if gender value is f,m or d
        if customer_details[2] not in ["f", "m", "d"]:
            raise ValueError(
                f"You entered {customer_details[2]} as third value."\
                " Third value has to be 'f','m' or 'd' for gender"
            )

    except ValueError as e:
        print(f"Invalid data:\n{e}.\nPlease try again.\n")
        return False

    return True


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
        styles = ["a) Microcar", "b) Hatchback", "c) Sedan", 
                  "d) SUV", "e) Convertable\n"]

        print(*styles, sep="\n")

        type_choices = input("Only select one letter [a, b, c, d, e]: \n")

        customer_choice = type_choices.lower().strip()
        print("Validating entered value...\n")

        if validate_type_choice(customer_choice):
            print(f"Entry '{customer_choice}' is valid. Processing data...\n")
            break

        get_type_options(customer_choice)

    return customer_choice


def validate_type_choice(customer_choice):
    """
    Function to validate if the user input given is valid.
    """
    try:
        if customer_choice not in ["a", "b", "c", "d", "e"]:
            raise ValueError(
                f"You entered '{customer_choice}'. \
                     \nOnly letters from a-f are valid"
            )
    except ValueError as e:
        print(f"Entry not valid:\n{e}, please try again.\n")
        return False

    return True


def get_type_options(customer_type):
    """
    Function to retrieve data from the options worksheet and compare 
    the options with the users input. 
    """
    if customer_type == "a":
        car_type = "microcar"

    elif customer_type == "b":
        car_type = "hatchback"
    
    elif customer_type == "c":
        car_type = "sedan"

    elif customer_type == "d":
        car_type = "suv"

    elif customer_type == "e":
        car_type = "convertible"
     
    print(f"The following options are {car_type.capitalize()}s:\n")

    # retrieve all options from worksheet options
    all_options = SHEET.worksheet("options")
    options = all_options.get_all_records()
    
    # for loop itterates through all options and matches this with user input
    for option in options:
        if option["Type"] == car_type:
            print(option)

              
intro()
details = get_customer_details()
customer_details = [detail for detail in details]
update_customer_details_worksheet(customer_details)
customer_type = select_car_type()
get_type_options(customer_type)
