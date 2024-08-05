# A script for simplifying characters.csv details for Mantella

import csv
import os
import logging
import time

def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

def extract_sentences(description, num_sentences):
    """Extract the specified number of sentences from the description."""
    sentences = description.split('.')
    extracted = '.'.join(sentences[:num_sentences]) + '.'
    return extracted.strip()

def get_num_sentences():
    """Ask the user how many sentences to include in the description."""
    while True:
        try:
            num_sentences = int(input("How many sentences should be used for the description? "))
            if num_sentences > 0:
                return num_sentences
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")

def process_fallout4_characters(input_file, num_sentences):
    """Process Fallout 4 character details."""
    
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
                
                wiki_and_desc = row[0]
                description = row[1]
                details = row[2:]
                
                extracted_description = extract_sentences(description, num_sentences)
                
                combined_line = [wiki_and_desc, extracted_description] + details
                
                writer.writerow(combined_line)

        logging.info(f"Processed Fallout 4 file saved as: {output_file}")
    except FileNotFoundError:
        logging.error(f"Input file not found: {input_file}")
    except Exception as e:
        logging.error(f"An error occurred while processing the file: {e}")

def process_skyrim_characters(input_file, num_sentences):
    """Process Skyrim character details."""
    
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

                name_and_voice = row[0] + ',' + row[1]
                bio = row[2]
                bio_url = row[3]
                additional_details_index = 4 if bio_url.startswith('http') else 3

                extracted_description = extract_sentences(bio, num_sentences)

                additional_details = row[additional_details_index:]

                combined_line = [name_and_voice, extracted_description, ''] + additional_details

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
    
    num_sentences = get_num_sentences()
    
    if 'fallout4_characters.csv' in csv_files:
        process_fallout4_characters('fallout4_characters.csv', num_sentences)
    elif 'skyrim_characters.csv' in csv_files:
        process_skyrim_characters('skyrim_characters.csv', num_sentences)
    else:
        logging.error("No known CSV files found. Please ensure either 'fallout4_characters.csv' or 'skyrim_characters.csv' is present.")
        time.sleep(2)  # Pause for 2 seconds

def main():
    setup_logging()
    detect_and_process_file()

if __name__ == '__main__':
    main()