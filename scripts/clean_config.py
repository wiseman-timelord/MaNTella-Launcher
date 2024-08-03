import time
import os
import shutil

# Define global variables for the file name and location
FILE_NAME = 'config.ini'
FILE_LOCATION = '.\\'

def check_and_streamline_ini():
    # Construct the full file path using the global variables
    file_path = os.path.join(FILE_LOCATION, FILE_NAME)
    backup_path = os.path.join(FILE_LOCATION, 'config.bak')

    # Check if the file exists
    if not os.path.exists(file_path):
        print("Critical Error: File not found.")
        time.sleep(5)
        return

    # Open the original file and read all lines
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Initialize counters
    blank_line_count = 0
    comment_line_count = 0

    # Check the file for blank lines and commented lines
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            blank_line_count += 1
        elif stripped_line.startswith(';'):
            comment_line_count += 1

    # Report initial findings
    print(f"- Blank lines: {blank_line_count}")
    print(f"- Commented lines: {comment_line_count}")
    time.sleep(1)

    # Determine if any processing is needed
    if blank_line_count == 0 and comment_line_count == 0:
        print("Cleaning Not Required.")
        time.sleep(2)
        return

    # Create a backup of the original file
    try:
        shutil.copy(file_path, backup_path)
        print("Backup Successfully Created: .\config.bak.")
        time.sleep(1)
    except Exception as e:
        print(f"Critical Error: Failed to create backup. Error: {e}")
        time.sleep(5)
        return

    print("Processing: Removing clutter...")
    time.sleep(1)

    # Initialize a list to hold the processed lines
    processed_lines = []

    # Process the lines to remove blanks and comments
    for line in lines:
        stripped_line = line.strip()
        # Retain non-blank, non-commented lines (keep key-value pairs and section headers)
        if stripped_line and not stripped_line.startswith(';'):
            processed_lines.append(line)

    # Write the processed lines back to the file
    try:
        with open(file_path, 'w') as file:
            file.writelines(processed_lines)
        print("Success: File processed and saved.")
        time.sleep(2)
    except Exception as e:
        print(f"Critical Error: Failed to write file. Error: {e}")
        time.sleep(5)

# Run the function using the global file name and location
check_and_streamline_ini()
