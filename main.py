"""
    This file is designed to format the provided text files into
    a csv format.
"""

import os
import re
from colorama import Fore

# Program Settings
INPUT_FOLDER = "./input"
OUTPUT_FOLDER = "./output"
PROGRAM_NAME = "Mass Text to CSV"

def empty_directory(directory, remove=True):
    """
        This function is used to empty a directory
    """

    # Loop through all the files in the directory
    for file in os.listdir(directory):
        # Gets the file path
        file_path = os.path.join(directory, file)
        try:
            # Checks if the file is a file
            if os.path.isfile(file_path):
                # Removes the file
                os.remove(file_path)
            else:
                # Removes the directory
                empty_directory(file_path)
                os.rmdir(file_path)
        except PermissionError:
            print(f"Failed to delete file: {file_path}")

    # Checks if the directory should be removed
    if remove is True:
        os.rmdir(directory)


def process_row(row):
    """
        This function is used to separate the data in a row
    """

    # Removes the whitespace from the start and end of the row
    row = row.strip()
    # Splits the row into a list
    row = re.sub(r"\s{1,}", ",", row)
    # Adds a new line to the end of the row
    row = f"{row}\n"

    return row

def process_text_file(file_name=""):
    """
        This function is used to process a file from txt to csv
    """

    file_data = []

    # Opens the file in read mode
    with open(file_name, "r", encoding="utf-8") as file:
        # Loops through all the lines in the file
        while True:
            line = file.readline()

            # Checks if the line is empty
            if line == "":
                break

            # Processes the row
            row = process_row(line)
            # Adds the row to the file data
            file_data.append(row)

    # Joins the file data into a string
    file_data = "".join(file_data)

    return file_data

def get_files_from_directory(directory):
    """
        This function is used to get all the files from a directory
    """

    files = []

    # Loops through all the files in the directory
    for file in os.listdir(directory):
        # Checks if the file is a text file
        if file.endswith(".txt"):
            # Adds the file to the list
            files.append(file)

    return files

def process_files(add_headers=False):
    """
        This function is used to process all the files in the input folder
    """

    files = get_files_from_directory(INPUT_FOLDER)

    if len(files) == 0:
        print(f"\n{Fore.RED}No files found in the input folder{Fore.RESET}\n")
        return

    headers = []

    if add_headers is True:
        print("\nColumn Settings:\n\nType exit to stop adding columns\n")
        column_count = 1

        while True:
            column = input(f"{Fore.GREEN}Enter column {column_count} name: {Fore.RESET}")

            if column == "exit":
                break

            if re.fullmatch(r"([A-z-0-9]{2,})", column):
                headers.append(column)
                column_count += 1
            else:
                print(f"\n{Fore.RED}Invalid column name{Fore.RESET}\n")
                continue

        headers = ",".join(headers)

    for file in files:
        print(f"\n{Fore.GREEN}Processing file: {Fore.RESET}", file)

        # Gets the file path
        file_path = os.path.join(INPUT_FOLDER, file)
        # Processes the file
        file_data = process_text_file(file_path)

        # Replace the file extension with csv
        new_file_name = file.replace(".txt", ".csv")

        # Gets the new file path
        new_file_path = os.path.join(OUTPUT_FOLDER, new_file_name)

        # Opens the file in write mode
        with open(new_file_path, "w", encoding="utf-8") as new_file:
            # Checks if the headers should be added
            if add_headers is True:
                # Adds the headers to the file
                new_file.write(headers + "\n")

            # Adds the file data to the file
            new_file.write(file_data)

        print(f"{Fore.GREEN}Processed: {Fore.RESET}", new_file_name)

def main():
    """
        This function is used to run the program
    """

    # Checks if the input folder does not exist
    if not os.path.exists(INPUT_FOLDER):
        # Creates the input folder
        try:
            os.mkdir(INPUT_FOLDER)
        except PermissionError:
            print(f"\n{Fore.RED}Permission denied to create input folder{Fore.RESET}\n")
            return

    # Checks if the output folder does not exist
    if not os.path.exists(OUTPUT_FOLDER):
        # Creates the output folder
        try:
            os.mkdir(OUTPUT_FOLDER)
        except PermissionError:
            print(f"\n{Fore.RED}Permission denied to create output folder{Fore.RESET}\n")
            return

    # Creates a welcome message
    welcome_message = f"Welcome to {PROGRAM_NAME}"
    # Formats the menu with its options
    menu = f"\n{Fore.BLUE}{welcome_message:^40}{Fore.RESET}\n\n"
    menu += f"{Fore.MAGENTA}[1]:{Fore.CYAN} Convert all files in the input folder\n"
    menu += f"{Fore.MAGENTA}[2]:{Fore.CYAN} Convert all files in the input folder and \
add column names\n"
    menu += f"{Fore.MAGENTA}[3]:{Fore.CYAN} Exit{Fore.RESET}\n\n"

    # Loops until the user exits the program
    while True:
        # Prints the menu
        print(menu)
        # Gets the user input
        choice = input(f"\n{Fore.GREEN}Enter your choice: {Fore.RESET}")

        # Converts the choice to an integer
        try:
            choice = int(choice)
        except ValueError:
            message = f"{Fore.RED}"
            message += f"\nPlease type in a numeric value for the menu option.{Fore.RESET}\n"
            print(message)
            continue

        if choice == 1:
            # Empty the output folder
            empty_directory(OUTPUT_FOLDER, False)
            # Process the files
            process_files()
        elif choice == 2:
            # Empty the output folder
            empty_directory(OUTPUT_FOLDER, False)
            # Process the files with headers
            process_files(True)
        elif choice == 3:
            # Exits the program
            break

    print(f"\n{Fore.GREEN}Exiting...{Fore.RESET}\n")

if __name__ == "__main__":
    main()
