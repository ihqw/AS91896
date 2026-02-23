import json
import os
import ctypes
from colorama import Fore, init

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "data", "data.json") # define data file path to save repeeating

ctypes.windll.kernel32.SetConsoleTitleW("Contact Manager CLI") # Set window title to a string rather then the file path.
init(autoreset=True) # disable colorama setting all colors to a specific one.

def view_data():
    try:
        with open(file_path, 'r') as f: # read the file 
            data = json.load(f)
        for person in data:
                print(f"{person['name']}: {', '.join(person['phone_numbers'])}") # print the details of all contacts
        return data
    except Exception as e:
        print(f'Error Message: {e}') # print potential errors
    return

def get_valid_contact():
    while True:
        name = input('Enter contacts name: ')
        if not name:
            print(Fore.RED + 'No input given.')
            continue

        number = input('Enter contacts number: ').strip()
        if not number:
            print(Fore.RED + 'No input given.')
            continue

        if not number.isdigit(): # check if number is actually a digit
            print(Fore.RED + 'Please enter a proper number.')
            continue

        return name, number # return validated variables

def add_contact(name, number):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                contacts = json.load(f)
            except Exception as e:
                print(f'error: {e}') # print error message
    else:
        contacts = []

    contacts.append({
        "name": name,
        "phone_numbers": [number]
    })

    with open(file_path, 'w') as f: # writing new contact to data.json file
        json.dump(contacts, f, indent=4)

def search():
    while True:
        user_input = input('Enter a name or number to search for: ').strip()
        if not user_input:
            print(Fore.RED + 'No input given.')
            continue
        break
    with open(file_path, 'r') as f:
        data = json.load(f)

    result = next((
        item for item in data
        if any(user_input.lower() in str(value).lower() for value in item.values())
    ), None)

    if result:
        print(Fore.GREEN + f"Contact found: {result}")
    else:
        print(Fore.RED + "No contact found with provided details.")

print(Fore.YELLOW + ' Contact Manager CLI')
print(Fore.YELLOW + ' For further assistance run the \'help\' command.\n')

while True:
    command = input('> ').lower() # set all input to lowercase to make command handling easier
    match command:
        case "search":
            search()

        case "view":
            view_data()

        case "add":
            name, number = get_valid_contact()
            add_contact(name, number) # pass validated arguements 
            print(Fore.GREEN + f'Successfully added {name} as a contact!')

        case "exit":
            break # exit command

        case "help":
            print(Fore.YELLOW + 'The following commands are:\n 1. View (view all contacts)\n 2. Search (search through contacts)\n 3. Add (adds new contact credentials)') # useful help commamnd

        case _:
            print(Fore.RED + f'Unknown command: "{command}"')

    if not command:
        print('No input given.') # prevent empty input