# A script for simplifying characters.csv details for Mantella

# Imports
import csv
import os
import logging
import time

# Functions...
def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

def extract_first_sentence(description):
    """Extract the first sentence from the description."""
    if '.' in description:
        return description.split('.')[0] + '.'
    return description

def process_fallout4_characters(input_file):
    """Process Fallout 4 character details."""
    
    # Create the output filename by adding '_lite' before the file extension
    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_lite{ext}"
    
    try:
        with open(input_file, mode='r', encoding='utf-8') as infile, \
             open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
            
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            
            for row in reader:
                if len(row) < 3:
                    logging.warning(f"Skipping malformed row: {row}")
                    continue
                
                # Get the wiki and description part
                wiki_and_desc = row[0]
                description = row[1]
                details = row[2:]
                
                # Extract the first sentence from the description
                first_sentence = extract_first_sentence(description)
                
                # Reconstruct the combined line
                combined_line = [wiki_and_desc, first_sentence] + details
                
                # Write the combined line to the new CSV file
                writer.writerow(combined_line)

        logging.info(f"Processed Fallout 4 file saved as: {output_file}")
    except FileNotFoundError:
        logging.error(f"Input file not found: {input_file}")
    except Exception as e:
        logging.error(f"An error occurred while processing the file: {e}")

def process_skyrim_characters(input_file):
    """Process Skyrim character details."""
    
    # Create the output filename by adding '_lite' before the file extension
    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_lite{ext}"
    
    try:
        with open(input_file, mode='r', encoding='utf-8') as infile, \
             open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
            
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            for row in reader:
                if len(row) < 5:
                    logging.warning(f"Skipping malformed row: {row}")
                    continue

                # Extract relevant parts
                name_and_voice = row[0] + ',' + row[1]
                bio = row[2]
                # Identify the start of the additional details by looking for a URL
                bio_url = row[3]
                additional_details_index = 4 if bio_url.startswith('http') else 3

                # Extract the first sentence from the bio
                first_sentence = extract_first_sentence(bio)

                # Extract additional details, ensuring the length matches the expected columns
                additional_details = row[additional_details_index:]

                # Reconstruct the combined line
                combined_line = [name_and_voice, first_sentence, ''] + additional_details

                # Write the combined line to the new CSV file
                writer.writerow(combined_line)

        logging.info(f"Processed Skyrim file saved as: {output_file}")
    except FileNotFoundError:
        logging.error(f"Input file not found: {input_file}")
    except Exception as e:
        logging.error(f"An error occurred while processing the file: {e}")

def detect_and_process_file():
    """Detect which CSV file is present and process it accordingly."""
    files = os.listdir('.')
    csv_files = [file for file in files if file.endswith('.csv')]
    
    # Detect the file
    if 'fallout4_characters.csv' in csv_files:
        process_fallout4_characters('fallout4_characters.csv')
    elif 'skyrim_characters.csv' in csv_files:
        process_skyrim_characters('skyrim_characters.csv')
    else:
        logging.error("No known CSV files found. Please ensure either 'fallout4_characters.csv' or 'skyrim_characters.csv' is present.")
        time.sleep(2)  # Pause for 2 seconds

# Main Loop
def main():
    setup_logging()
    detect_and_process_file()

# Entry Point
if __name__ == '__main__':
    main()
