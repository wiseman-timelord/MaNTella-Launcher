import configparser
import os
import sys
import time
import shutil
import traceback

def verbose_print(message):
    print(message, file=sys.stderr)
    sys.stderr.flush()

def delay(seconds=1):
    time.sleep(seconds)

verbose_print("Script started")

# Global variables
FILE_NAME = 'config.ini'
OUTPUT_FILE = 'main-wt.txt'  # New output file for batch script
game = "Skyrim"
optimization = "Default"
custom_token_count = 2048
game_folders = {}
mod_folders = {}
xvasynth_folder = ""

verbose_print(f"Working Folder: {os.getcwd()}")
verbose_print(f"Config File: {os.path.abspath(FILE_NAME)}")
delay()

# Optimization presets
optimization_presets = {
    "Default": {"max_tokens": 250, "max_response_sentences": 999, "temperature": 1.0},
    "Faster": {"max_tokens": 100, "max_response_sentences": 1, "temperature": 0.4},
    "Medium": {"max_tokens": 150, "max_response_sentences": 2, "temperature": 0.5},
    "Quality": {"max_tokens": 200, "max_response_sentences": 3, "temperature": 0.6}
}

def clean_config():
    verbose_print("Starting config cleaning process...")
    delay()
    
    if not os.path.exists(FILE_NAME):
        verbose_print(f"Config file '{FILE_NAME}' not found.")
        delay(3)
        return

    with open(FILE_NAME, 'r') as file:
        lines = file.readlines()

    blank_line_count = sum(1 for line in lines if not line.strip())
    comment_line_count = sum(1 for line in lines if line.strip().startswith(';'))

    verbose_print(f"Found {blank_line_count} blank lines and {comment_line_count} comment lines.")

    if blank_line_count == 0 and comment_line_count == 0:
        verbose_print("Config file is already clean. No changes needed.")
        delay(2)
        return

    backup_path = 'config.bak'
    try:
        shutil.copy(FILE_NAME, backup_path)
        verbose_print(f"Backup created: {backup_path}")
    except Exception as e:
        verbose_print(f"Error creating backup: {str(e)}")
        delay(3)
        return

    verbose_print("Removing clutter and formatting...")
    delay()
    
    processed_lines = []
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line and not stripped_line.startswith(';'):
            if stripped_line.startswith('[') and i > 0 and processed_lines:
                processed_lines.append('\n')
            processed_lines.append(line)

    try:
        with open(FILE_NAME, 'w') as file:
            file.writelines(processed_lines)
        verbose_print("Config file cleaned and saved successfully.")
        delay(2)
    except Exception as e:
        verbose_print(f"Error writing cleaned config: {str(e)}")
        delay(3)

def read_config():
    verbose_print("Reading config file...")
    global game, optimization, custom_token_count, game_folders, mod_folders, xvasynth_folder
    config = configparser.ConfigParser()

    try:
        config.read(FILE_NAME)
    except configparser.Error as e:
        verbose_print(f"Error reading config.ini file: {str(e)}")
        delay(3)
        return
    
    # Get the game name
    game = config.get("Game", "game", fallback="Skyrim")

    # Fetch paths based on sections and keys
    game_folders = {
        "skyrim": config.get("Paths", "skyrim_folder", fallback="Not set"),
        "skyrimvr": config.get("Paths", "skyrimvr_folder", fallback="Not set"),
        "fallout4": config.get("Paths", "fallout4_folder", fallback="Not set"),
        "fallout4vr": config.get("Paths", "fallout4vr_folder", fallback="Not set"),
    }

    mod_folders = {
        "skyrim": config.get("Paths", "skyrim_mod_folder", fallback="Not set"),
        "skyrimvr": config.get("Paths", "skyrimvr_mod_folder", fallback="Not set"),
        "fallout4": config.get("Paths", "fallout4_mod_folder", fallback="Not set"),
        "fallout4vr": config.get("Paths", "fallout4vr_mod_folder", fallback="Not set"),
    }

    # Set xVASynth folder
    xvasynth_folder = config.get("Paths", "xvasynth_folder", fallback="Not set")

    # Fetch Language Model settings
    custom_token_count = int(config.get("LanguageModel.Advanced", "custom_token_count", fallback="2048"))
    
    # Check for optimization preset
    max_tokens = int(config.get("LanguageModel.Advanced", "max_tokens", fallback="250"))
    max_response_sentences = int(config.get("LanguageModel", "max_response_sentences", fallback="999"))
    temperature = float(config.get("LanguageModel.Advanced", "temperature", fallback="1.0"))

    for preset, values in optimization_presets.items():
        if (max_tokens == values["max_tokens"] and
            max_response_sentences == values["max_response_sentences"] and
            abs(temperature - values["temperature"]) < 0.01):
            optimization = preset
            break
    else:
        optimization = "Default"

    verbose_print(f"Read Keys: config.ini.")
    delay(2)

def write_config():
    verbose_print("Writing config file...")
    config = configparser.ConfigParser()
    
    try:
        config.read(FILE_NAME)
    except configparser.Error as e:
        verbose_print(f"Error reading existing config for writing: {str(e)}")
        delay(3)
        return
    
    if "Game" not in config:
        config["Game"] = {}
    config["Game"]["game"] = game
    
    if "LanguageModel.Advanced" not in config:
        config["LanguageModel.Advanced"] = {}
    config["LanguageModel.Advanced"]["custom_token_count"] = str(custom_token_count)
    
    preset = optimization_presets[optimization]
    config["LanguageModel.Advanced"]["max_tokens"] = str(preset["max_tokens"])
    config["LanguageModel.Advanced"]["temperature"] = str(preset["temperature"])
    
    if "LanguageModel" not in config:
        config["LanguageModel"] = {}
    config["LanguageModel"]["max_response_sentences"] = str(preset["max_response_sentences"])
    
    try:
        with open(FILE_NAME, 'w') as configfile:
            config.write(configfile)
    except Exception as e:
        verbose_print(f"Error writing config: {str(e)}")
        delay(3)

    delay(2)

def write_output_file(exit_code, xvasynth_path):
    verbose_print(f"Writing output file '{OUTPUT_FILE}' with exit_code={exit_code} and xvasynth_path={xvasynth_path}")
    try:
        with open(OUTPUT_FILE, 'w') as output_file:
            output_file.write(f"exit_code={exit_code}\n")
            output_file.write(f"xvasynth_path={xvasynth_path}\n")
        verbose_print("Output file written successfully")
    except Exception as e:
        verbose_print(f"Error writing output file: {str(e)}")
        delay(3)

def display_menu():
    verbose_print("Displaying menu...")
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 120)
    print("                                        Mantella xVASynth, Optimizer / Launcher")
    print("-" * 120)
    print(f"\n\n\n")
    print(f"                                               1. Game Used: {game}\n")
    print(f"                                               2. Optimization: {optimization}\n")
    print(f"                                               3. Context Length: {custom_token_count}\n")
    print(f"\n\n\n")
    print("-" * 120)
    print()
    game_key = game.lower().replace(" ", "")
    print(f"\n")
    print(f"                                   {game}_folder = {game_folders.get(game_key, 'Not set')}")
    print(f"                                   {game}_mod_folder = {mod_folders.get(game_key, 'Not set')}")
    print(f"                                   xvasynth_folder = {xvasynth_folder}")
    print(f"\n")
    print("-" * 120)

def toggle_game():
    verbose_print("Toggling game...")
    global game
    games = ["Skyrim", "SkyrimVR", "Fallout4", "Fallout4VR"]
    game = games[(games.index(game) + 1) % len(games)]
    delay()

def toggle_optimization():
    verbose_print("Toggling optimization...")
    global optimization
    optimizations = list(optimization_presets.keys())
    optimization = optimizations[(optimizations.index(optimization) + 1) % len(optimizations)]
    delay()

def toggle_context_length():
    verbose_print("Toggling context length...")
    global custom_token_count
    context_lengths = [2048, 4096, 8096, 16384]
    custom_token_count = context_lengths[(context_lengths.index(custom_token_count) + 1) % len(context_lengths)]
    delay()

def main():
    verbose_print("Entering main function")
    try:
        clean_config()
        read_config()
        
        while True:
            display_menu()
            choice = input("Selection, Run Mantella/xVASynth = R, Program Options 1-3, Exit and Save = X: ").strip().upper()
            
            if choice == '1':
                toggle_game()
            elif choice == '2':
                toggle_optimization()
            elif choice == '3':
                toggle_context_length()
            elif choice == 'R':
                write_config()
                verbose_print("Settings saved. Proceeding to run Mantella/xVASynth...")
                write_output_file(0, xvasynth_folder)  # Save relevant values
                return 0, xvasynth_folder
            elif choice == 'X':
                write_config()
                verbose_print("Settings saved. Exiting...")
                write_output_file(1, "")  # Save exit signal
                return 1, ""
            else:
                verbose_print("Invalid selection. Please try again.")
    except Exception as e:
        verbose_print(f"An unexpected error occurred: {str(e)}")
        verbose_print("Traceback:")
        verbose_print(traceback.format_exc())
        write_output_file(1, "")  # Ensure an error exit signal is saved
        delay(3)
        return 1, ""

if __name__ == "__main__":
    verbose_print("Script execution started")
    try:
        exit_code, xvasynth_path = main()
        print(f"{exit_code},{xvasynth_path}", file=sys.stdout)
        sys.stdout.flush()
        verbose_print(f"Final output: exit_code={exit_code}, xvasynth_path={xvasynth_path}")
    except Exception as e:
        verbose_print(f"An unexpected error occurred in the main execution: {str(e)}")
        verbose_print("Traceback:")
        verbose_print(traceback.format_exc())
        print("1,", file=sys.stdout)
        sys.stdout.flush()
    verbose_print("Script execution ended")
    sys.exit(exit_code)
