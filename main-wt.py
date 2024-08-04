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
    verbose_print("Starting config cleaning...")
    delay()
    
    if not os.path.exists(FILE_NAME):
        verbose_print(f"Config file '{FILE_NAME}' not found.")
        delay(3)
        return

    with open(FILE_NAME, 'r') as file:
        lines = file.readlines()

    comment_line_count = sum(1 for line in lines if line.strip().startswith(';'))

    verbose_print(f"Found {comment_line_count} comment lines.")

    if comment_line_count == 0:
        verbose_print("Config Already Clean.")
        delay(2)
        return

    backup_path = 'config.bak'
    if not os.path.exists(backup_path):
        try:
            shutil.copy(FILE_NAME, backup_path)
            verbose_print(f"Backup created: {backup_path}")
        except Exception as e:
            verbose_print(f"Error creating backup: {str(e)}")
            delay(3)
            return
    else:
        verbose_print(f"Backup file {backup_path} already exists. Skipping backup.")

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
        verbose_print("Config cleaned and saved.")
        delay(2)
    except Exception as e:
        verbose_print(f"Error writing config: {str(e)}")
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
    verbose_print(f"Writing output file: exit_code={exit_code}, xvasynth_path={xvasynth_path}")
    try:
        with open(OUTPUT_FILE, 'w') as f:
            f.write(f"exit_code={exit_code}\nxvasynth_path={xvasynth_path}")
        verbose_print(f"Output file written successfully: {OUTPUT_FILE}")
    except Exception as e:
        verbose_print(f"Error writing output file: {str(e)}")


def check_and_update_prompts():
    verbose_print("Checking Prompts")
    config = configparser.ConfigParser()
    config.read(FILE_NAME)

    prompt_keys = [
        "skyrim_prompt", "skyrim_multi_npc_prompt", "fallout4_prompt", 
        "fallout4_multi_npc_prompt", "radiant_start_prompt", "radiant_end_prompt", 
        "memory_prompt", "resummarize_prompt"
    ]

    updated_prompts = {
        "skyrim_prompt": "You are {name} from Skyrim. This is your background:{bio}, stay in character. You are having a conversation with(the player), in {location} and in Skyrim and at {time_group} time. The conversation is in {language}. The situation so far is... {conversation_summary}. Respond as {name}. This response will be spoken aloud, so keep responses concise, and avoid, numbered lists or descriptions of actions, instead speech ONLY. Do not use symbols of any form in your output.",
        "skyrim_multi_npc_prompt": "The following is a conversation between {names_w_player} from Skyrim, in {location} and at {time_group} time. Backgrounds: {bios}, utilize all characters. Their conversation histories: {conversation_summaries}. Respond as {names}. This response will be spoken aloud, so keep responses concise, and avoid, numbered lists or descriptions of actions, instead speech ONLY. Do not use symbols in any form in your output.",
        "fallout4_prompt": "You are {name} in Fallout4. This is your background: {bio}. You're having a conversation with (the player) in {location}. The time is {time_group} time. The conversation is in {language}. The situation so far is... {conversation_summary}. This response will be spoken aloud, so keep responses concise, and avoid, numbered lists or descriptions of actions, instead speech ONLY. Do not use symbols in any form in your output.",
        "fallout4_multi_npc_prompt": "The following is a conversation between {names_w_player} from Fallout 4, in {location} and at {time_group} time. Their backgrounds: {bios}. Their conversation histories: {conversation_summaries}. Respond as {names}. and avoid, numbered lists or descriptions of actions, instead speech ONLY. The conversation is in {language}. Do not use symbols in any form in your output. ",
        "radiant_start_prompt": "Start or continue a conversation topic (skip greetings). Shift topics if current ones lose steam. Steer toward character revelations or drive previous conversations forward. The conversation is in {language}. Do not use symbols in any form in your output.",
        "radiant_end_prompt": "In {language} and with a maximum of 125 text characters, wrap up the current topic naturally. No need for formal goodbyes as no one is leaving.  The summarization is in {language}. Do not use symbols of any kind in your output.",
        "memory_prompt": "In {language} and with a maximum of 250 text characters, summarize the conversation between {name} (assistant) and the player (user)/others in {game}, capturing the essence of in-game events. Ignore communication mix-ups like mishearings. The summarization is in {language}. Do not use symbols in any form in your output.",
        "resummarize_prompt": "In {language} and with a maximum of 500 text characters and in single short paragraphs, summarize the conversation history between {name} (assistant) and the player (user)/others in {game}. Each paragraph is a separate conversation.  The summarization is in {language}. Do not use symbols in any form in your output."
    }

    needs_update = False
    if 'Prompt' not in config:
        verbose_print("'Prompt' section not found in config. Creating it.")
        config['Prompt'] = {}
        needs_update = True
    else:
        for key in prompt_keys:
            if key not in config['Prompt']:
                verbose_print(f"Prompt key '{key}' not found in config. Will update.")
                needs_update = True
                break
            elif config['Prompt'][key].strip() != updated_prompts[key].strip():
                verbose_print(f"Prompt '{key}' needs updating.")
                verbose_print(f"Current: {config['Prompt'][key]}")
                verbose_print(f"Updated: {updated_prompts[key]}")
                if key == "resummarize_prompt":
                    verbose_print("Detailed comparison of resummarize_prompt:")
                    current = config['Prompt'][key].strip()
                    updated = updated_prompts[key].strip()
                    verbose_print(f"Length of current: {len(current)}")
                    verbose_print(f"Length of updated: {len(updated)}")
                    for i, (c, u) in enumerate(zip(current, updated)):
                        if c != u:
                            verbose_print(f"Difference at position {i}: '{c}' vs '{u}'")
                            break
                needs_update = True
                break

    if needs_update:
        verbose_print("Optimizing Prompts..")
        for key, value in updated_prompts.items():
            config['Prompt'][key] = value
        
        try:
            with open(FILE_NAME, 'w') as configfile:
                config.write(configfile)
            verbose_print("..Prompts Optimized.")
        except Exception as e:
            verbose_print(f"Error writing updated prompts to config file: {str(e)}")
            delay(3)
    else:
        verbose_print("Prompts Already Optimized.")
        delay(1)

def display_title():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 120)
    print("                                        Mantella xVASynth, Optimizer / Launcher")
    print("-" * 120)
    print(f"")
    
def display_menu():
    display_title()
    print(f"\n\n")
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
        check_and_update_prompts()
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
                display_title()
                write_config()
                verbose_print("Settings saved. Proceeding to run Mantella/xVASynth...")
                write_output_file(0, xvasynth_folder)  # Save relevant values
                return 0, xvasynth_folder
            elif choice == 'X':
                display_title()
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
