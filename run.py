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

# variable to access customer worksheet
customers_worksheet = SHEET.worksheet("customers")


def intro():
    """
    Introduction to the app
    """
    print("Welcome to Electric Vehicle Picker!\n")
    print(("Follow the instructions given to get a recommendation and save"
           " the customer data for further analysis.\n"))


def get_customer_details():
    """
    Get the customers' full name, age, gender
    and the info if they already drive electric.
    """
    while True:
        print(("Please enter the 4 customer details as discribed below\n"
               "with NO spaces between the values:\n"))
        details = ["1. Full Name: enter customers first name and surname",
                   "2. Age: enter customers' age",
                   "3. Gender: enter m,f or d",
                   "4. Already drive electric? : enter yes or no\n"]

        print(*details, sep="\n\n")
        print("Example: June Austin,35,f,no\n")

        details_str = input("Enter customer details here: \n")

        customer_details = details_str.split(",")

        if validate_data_input(customer_details):
            print("\nData valid!")
            break

    add_id(customer_details)
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
                f"You entered {customer_details[0]} as first value."
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
                f"You entered {customer_details[1]} as second value."
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
                f"You entered {customer_details[2]} as third value."
                " Third value has to be m,f or d for gender"
            )

        # check if gender value is f,m or d
        if customer_details[2] not in ["f", "m", "d"]:
            raise ValueError(
                f"You entered {customer_details[2]} as third value."
                " Third value has to be 'f','m' or 'd' for gender.\n"
                "Don't forget to remove the space before the letter"
            )
        # check if value is yes or no
        if customer_details[3] not in ["yes", "no"]:
            raise ValueError(
                f"You entered {customer_details[3]} as forth value."
                " Answer question only with yes or no.\n"
                "Don't forget to remove the space before the yes/no"
            )

        if customer_details[3] == "":
            raise ValueError(
                f"You entered {customer_details[3]}.Only answer with yes or no"
            )

    except ValueError as e:
        print(f"Invalid data:\n{e}.\nPlease try again.\n")
        return False

    return True


def add_id(customer_details):
    """
    Function to add id to customer details
    """
    id_new = []
    id_customers = customers_worksheet.col_values(1)[-1]
    id_new = int(id_customers) + 1
    customer_details.insert(0, id_new)


def update_customer_details_worksheet(details):
    """
    Update customers worksheet, add new row with customer details
    """
    print("Updating customers worksheet...\n")
    customer_details = []
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
        print("\nValidating entered value...")

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
                     \nOnly letters from a-e are valid"
            )
    except ValueError as e:
        print(f"\nEntry not valid:\n{e}, please try again.\n")
        return False

    return True


def get_type_options(customer_type):
    """
    Function to retrieve data from the options worksheet and compare
    the options with the users input.
    """
    car_type = ""
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
    result = []
    for option in options:
        if option["Type"] == car_type:
            result = list(option.values())[0]
            print(result)


def main():
    """
    Function to run all program functions
    """
    intro()
    details = get_customer_details()
    customer_details = [detail for detail in details]
    update_customer_details_worksheet(customer_details)
    customer_type = select_car_type()
    car_options = get_type_options(customer_type)

    back_to_start()


def back_to_start():
    """
    Function to either start the programm from the beginning or
    end it with a short user message.
    """
    while True:
        print("\nIf you want to start from the beginning please enter 's'\n"
              "to exit the program enter 'e'.\n")
        back_options = input("Please enter input here: \n")

        if validate_back_to_start(back_options):
            print(f"\nEntry '{back_options}' is valid. Processing data...\n")
            start_or_exit(back_options)
            break

    return back_options


def validate_back_to_start(back_options):
    """
    Functiont to validate user input of back_to_start function.
    """
    try:
        if back_options not in ["e", "s"]:
            raise ValueError(
                f"You entered '{back_options}'. \
                     \nOnly 'e' for exit or 's' for start are valid"
            )
    except ValueError as e:
        print(f"\nEntry not valid:\n{e}, please try again.\n")
        return False

    return True


def start_or_exit(back_options):
    """
    Function to either start program again or exit program.
    """

    if back_options == 's':
        print("Restarting the program...\n")
        main()

    elif back_options == 'e':
        print("Thank you for using the e-vehicle app.")


main()
