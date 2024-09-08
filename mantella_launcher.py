# Script: .\launcher.py

# Imports
import os, sys, time, shutil, traceback, subprocess  # Common Imports
import configparser, json  # Config/Json Related

# Global variables
FILE_NAME = 'config.ini'
OUTPUT_FILE = '.\\data\\temporary_batch.txt'
game = "Skyrim"
optimization = "Default"
game_folders = {}
mod_folders = {}
xvasynth_folder = ""
model_id = ""
custom_token_count = 8192    # Default value
lmstudio_api_url = "http://localhost:1234/v1/models"
microphone_enabled = False
FILE_NAME = 'config.ini'
DEFAULT_FILE_PATHS = [
    FILE_NAME,
    os.path.join(os.environ.get('USERPROFILE', ''), 'Documents', 'My Games', 'Mantella', FILE_NAME)
]

# Initialization
def verbose_print(message):
    print(message, file=sys.stderr)
    sys.stderr.flush()

def delay(seconds=1):
    time.sleep(seconds)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

verbose_print(".\launcher.py Initialized.") 
delay()

# Optimization presets
optimization_presets = {
    "Default": {"max_tokens": 250, "max_response_sentences": 999, "temperature": 1.0},
    "Faster": {"max_tokens": 100, "max_response_sentences": 1, "temperature": 0.4},
    "Regular": {"max_tokens": 150, "max_response_sentences": 2, "temperature": 0.5},
    "Quality": {"max_tokens": 200, "max_response_sentences": 3, "temperature": 0.6}
}

def get_or_set_models_drive():
    json_file_path = os.path.join("data", "temporary_launcher.json")
    
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
    
    try:
        # Try to read the existing JSON file
        with open(json_file_path, 'r') as f:
            data = json.load(f)
            models_drive_letter = data.get('models_drive_letter')
        
        if models_drive_letter:
            verbose_print(f"Using saved models drive: {models_drive_letter}")
            return models_drive_letter
    except FileNotFoundError:
        verbose_print("No saved models drive found.")
    except json.JSONDecodeError:
        verbose_print("Error reading JSON file. Will create a new one.")
    
    # If we couldn't get the drive letter from the file, ask the user
    models_drive_letter = input("Enter the drive letter where your models are stored (e.g., C, D, E): ").upper()
    
    # Save the drive letter to the JSON file
    with open(json_file_path, 'w') as f:
        json.dump({'models_drive_letter': models_drive_letter}, f)
    
    verbose_print(f"Saved models drive: {models_drive_letter}")
    return models_drive_letter


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

def find_config_file():
    """Finds the config file in potential directories."""
    for path in DEFAULT_FILE_PATHS:
        if os.path.exists(path):
            return path
    return None

def read_config():
    verbose_print("Reading config file...")
    global game, optimization, custom_token_count, game_folders, mod_folders, xvasynth_folder, microphone_enabled
    config = configparser.ConfigParser()

    # Find the config file path
    config_path = find_config_file()
    if config_path:
        try:
            config.read(config_path)
        except configparser.Error as e:
            verbose_print(f"Error reading config.ini file: {str(e)}")
            delay(3)
            return
    else:
        verbose_print("No config file found. Using default settings.")
        delay(2)
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
        "skyrimvr": config.get("Paths", "skyrim_mod_folder", fallback="Not set"),
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
        if (
            max_tokens == values["max_tokens"]
            and max_response_sentences == values["max_response_sentences"]
            and abs(temperature - values["temperature"]) < 0.01
        ):
            optimization = preset
            break
    else:
        optimization = "Default"

    # Read microphone setting
    microphone_enabled = config.getboolean("Microphone", "microphone_enabled", fallback=False)

    verbose_print(f"Read Keys: config.ini.")
    delay(2)

def write_config():
    verbose_print("Writing config file...")
    global microphone_enabled
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
    config["LanguageModel"]["model"] = model_id
    
    if "Microphone" not in config:
        config["Microphone"] = {}
    config["Microphone"]["microphone_enabled"] = str(int(microphone_enabled))
    
    # Add the Speech section and tts_service key
    if "Speech" not in config:
        config["Speech"] = {}
    config["Speech"]["tts_service"] = "xVASynth"

    # Add the LM Studio API key
    if "LanguageModel.Advanced" not in config:
        config["LanguageModel.Advanced"] = {}
    config["LanguageModel.Advanced"]["llm_api"] = "http://localhost:1234/v1"
    
    try:
        with open(FILE_NAME, 'w') as configfile:
            config.write(configfile)
        verbose_print("Config file updated successfully.")
    except Exception as e:
        verbose_print(f"Error writing config: {str(e)}")
        delay(3)
    delay(2)

def write_output_file(exit_code):
    verbose_print(f"Writing output file")
    try:
        game_key = game.lower().replace(" ", "")
        game_folder = game_folders.get(game_key, "Not set")
        with open(OUTPUT_FILE, 'w') as f:
            f.write(f"exit_code={exit_code}\n")
            f.write(f"xvasynth_folder={xvasynth_folder}\n")  # Use the global xvasynth_folder
            f.write(f"game={game}\n")
            f.write(f"game_folder={game_folder}")
        verbose_print(f"Output file written successfully: {OUTPUT_FILE}")
    except Exception as e:
        verbose_print(f"Error writing output file: {str(e)}")

def read_temp_file():
    """Reads the .\data\temporary_batch.txt file to determine which model server to use."""
    verbose_print("Reading Model Server Choice...")
    server_choice = None

    try:
        with open(OUTPUT_FILE, 'r') as f:
            for line in f:
                if line.startswith("service="):
                    server_choice = line.split("=")[1].strip()
                    break
        verbose_print(f"Model server choice: {server_choice}")
    except FileNotFoundError:
        verbose_print(f"Temporary file '{OUTPUT_FILE}' not found.")
    except Exception as e:
        verbose_print(f"Error reading temporary file: {str(e)}")

    return server_choice

def get_or_set_models_drive():
    json_file_path = os.path.join("data", "temporary_launcher.json")
    
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
    
    try:
        # Try to read the existing JSON file
        with open(json_file_path, 'r') as f:
            data = json.load(f)
            models_drive_letter = data.get('models_drive_letter')
        
        if models_drive_letter:
            verbose_print(f"Using saved models drive: {models_drive_letter}")
            return models_drive_letter
    except FileNotFoundError:
        verbose_print("No saved models drive found.")
    except json.JSONDecodeError:
        verbose_print("Error reading JSON file. Will create a new one.")
    
    # If we couldn't get the drive letter from the file, ask the user
    models_drive_letter = input("Enter the drive letter where your models are stored (e.g., C, D, E): ").upper()
    
    # Save the drive letter to the JSON file
    with open(json_file_path, 'w') as f:
        json.dump({'models_drive_letter': models_drive_letter}, f)
    
    verbose_print(f"Saved models drive: {models_drive_letter}")
    return models_drive_letter

def fetch_model_details_ollama():
    global model_id
    config = configparser.ConfigParser()

    try:
        config.read(FILE_NAME)

        result = subprocess.run(['ollama', 'ps'], capture_output=True, text=True, check=True)
        output_lines = result.stdout.strip().split('\n')
        filtered_output = '\n'.join([line for line in output_lines if not line.startswith("failed to get console mode")])
        lines = [line for line in filtered_output.splitlines() if not line.startswith("failed to get console mode")]

        if len(lines) < 2:
            verbose_print("No models currently loaded in Ollama.")
            model_id = "No model loaded"
            return

        model_line = lines[1]
        verbose_print(f"Model line: {model_line}")

        model_parts = model_line.split()
        if len(model_parts) < 1:
            verbose_print(f"Unexpected format in 'ollama ps' output: {model_line}")
            model_id = "Unexpected model format"
            return

        model_name = model_parts[0].split(':')[0]
        verbose_print(f"Detected model name: {model_name}")

        model_folder_name = model_name.replace("IQ3_M-imat", "GGUF-IQ-Imatrix")

        models_drive_letter = get_or_set_models_drive()

        found = False
        for root, dirs, files in os.walk(f"{models_drive_letter}:\\"):
            verbose_print(f"Searching in directory: {root}")
            if model_folder_name in dirs:
                full_path = os.path.join(root, model_folder_name)
                verbose_print(f"Found model folder: {full_path}")

                path_parts = full_path.split(os.path.sep)
                if len(path_parts) >= 2:
                    author_folder = path_parts[-2]
                    model_folder = path_parts[-1]
                    model_id = f"{author_folder}\\{model_folder}"
                    verbose_print(f"Extracted model ID: {model_id}")

                    if "LanguageModel" not in config:
                        config["LanguageModel"] = {}
                    config["LanguageModel"]["model"] = model_id

                    with open(FILE_NAME, 'w') as configfile:
                        config.write(configfile)

                    verbose_print(f"Model Read: Ollama - {model_id}")
                    found = True
                    break
        
        if not found:
            verbose_print(f"Model folder not found for {model_folder_name}")
            model_id = "Model folder not found"

    except subprocess.CalledProcessError as e:
        verbose_print(f"Error running 'ollama ps' command: {e}")
        verbose_print(f"Command output: {e.stderr}")
        model_id = "Error running Ollama command"
    except Exception as e:
        verbose_print(f"Error fetching model details from Ollama: {str(e)}")
        traceback.print_exc()
        model_id = "Error occurred"

    delay(1)

def fetch_model_details_lmstudio():
    global model_id
    config = configparser.ConfigParser()

    try:
        config.read(FILE_NAME)
        try:
            result = subprocess.run(['curl', lmstudio_api_url], capture_output=True, text=True, check=True)
            model_data = json.loads(result.stdout)
            
            if 'data' in model_data and len(model_data['data']) > 0:
                full_id = model_data['data'][0]['id']
                model_id = full_id.rsplit('/', 1)[0]

                if "LanguageModel" not in config:
                    config["LanguageModel"] = {}
                config["LanguageModel"]["model"] = model_id

                with open(FILE_NAME, 'w') as configfile:
                    config.write(configfile)

                verbose_print(f"Model Read: LM Studio - {model_id}")
            else:
                verbose_print("No models currently loaded in LM Studio.")
                model_id = "No model loaded"
        except subprocess.CalledProcessError as e:
            verbose_print(f"Error running curl command: {e}")
            verbose_print(f"Curl output: {e.stderr}")
            model_id = "Error fetching model"
        except json.JSONDecodeError:
            verbose_print("Error parsing JSON from curl output")
            model_id = "Error parsing model data"
    except Exception as e:
        verbose_print(f"Error fetching model details: {str(e)}")
        traceback.print_exc()
        model_id = "Error occurred"

    delay(1)

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
        "skyrim_prompt": "You are {name} from Skyrim. this is your background: {bio}, stay in character. You are having a conversation with the Player, in {location} and in Skyrim and at {time_group} time. The situation so far is... {conversation_summary}. In, {language} and a maximum of 100 text characters, respond in 2 sentences as {name}, ensuring, 1 response sentence and 1 statement sentence. If the Player, offends or apologises or convinces to follow, either or both, of {names}, then the relevant individuals should start with relevantly, 'Offended:' or 'Forgiven:' or 'Follow:'. The response will be spoken aloud, so keep response concise, and remember speech ONLY, do not use, symbols such as asterisks or describe actions, in your output.",
        
        "skyrim_multi_npc_prompt": "The following is a conversation between, {names} from Skyrim and the Player, in {location} and at {time_group} time. Their backgrounds are: {bios}, utilize all NPC characters and stay in character. Their conversation histories: {conversation_summaries}. In, {language} and a maximum of 150  text characters, respond in multiple sentences as {names}, ensuring 1 sentence response from each of them. If the Player, offends or apologises or convinces to follow, either or both, of {names}, then the relevant individuals should start with relevantly, 'Offended:' or 'Forgiven:' or 'Follow:'. The response will be spoken aloud, so keep response concise, and remember speech ONLY, do not use, symbols such as asterisks or describe actions, in your output.",
        
        "fallout4_prompt": "You are {name} from Fallout 4, this is your background: {bio}, stay in character. You're having a conversation with the Player in {location}. The time is {time_group} time. The situation so far is... {conversation_summary}. In, {language} and a maximum of 100 text characters, respond in 2 sentences as {name}, ensuring, 1 response sentence and 1 statement sentence. If the Player, offends or apologises or convinces to follow, either or both, of {names}, then the relevant individuals should start with relevantly, 'Offended:' or 'Forgiven:' or 'Follow:'. The response will be spoken aloud, so keep response concise, and remember speech ONLY, do not use, symbols such as asterisks or describe actions, in your output.",
        
        "fallout4_multi_npc_prompt": "The following is a conversation between, {names} from Fallout 4 and the Player, in {location} and at {time_group} time. Their backgrounds are: {bios}, utilize all NPC characters and stay in character. Their conversation histories: {conversation_summaries}. In, {language} and a maximum of 150  text characters, respond in multiple sentences as {names}, ensuring 1 sentence response from each of them. If the Player, offends or apologises or convinces to follow, either or both, of {names}, then the relevant individuals should start with relevantly, 'Offended:' or 'Forgiven:' or 'Follow:'. The response will be spoken aloud, so keep response concise, and remember speech ONLY, do not use, symbols such as asterisks or describe actions, in your output.",
        
        "radiant_start_prompt": "Start or continue, a conversation relevant to, {name} and the Player and {game}, skip past any greetings. In, {language} and a maximum of 150 text characters, respond in 2 sentences as {name}, ensuring, 1 response sentence and 1 statement sentence. If the Player, offends or apologises or convinces to follow, either or both, of {names}, then the relevant individuals should start with relevantly, 'Offended:' or 'Forgiven:' or 'Follow:'. The response will be spoken aloud, so keep response concise, and remember speech ONLY, do not use, symbols such as asterisks or describe actions, in your output.",
        
        "radiant_end_prompt": "In, {language} and a maximum of 100 text characters, wrap up the current topic naturally. No need for formal goodbyes as no one is leaving. Keep the summary concise, and remember narration ONLY, do not use, symbols such as asterisks or describe actions, in your output.", 
        
        "memory_prompt": "In, {language} and a maximum of 200 text characters, summarize the conversation between, {name} and the Player and other NPCs present, capturing the essence of in-game events. Ignore communication mix-ups like mishearings. Keep the summary concise, and remember narration ONLY, do not use, symbols such as asterisks or describe actions, in your output.", 
        
        "resummarize_prompt": "In {language} and with a maximum of 500 text characters and in single short paragraphs, summarize the conversation history between {name} (assistant) and the Player (user)/others in {game}. Each paragraph is a separate conversation. Keep the summary concise, and remember narration ONLY, do not use, symbols such as asterisks or describe actions, in your output."
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
            elif len(config['Prompt'][key].strip()) != len(updated_prompts[key].strip()):
                verbose_print(f"Prompt '{key}' needs updating.")
                verbose_print(f"Current: {config['Prompt'][key]}")
                verbose_print(f"Updated: {updated_prompts[key]}")
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
    clear_screen()
    print("=" * 119)
    print("    MaNTella-Launcher")
    print("-" * 119)
    print("")

def display_menu_and_handle_input():
    global game, optimization, custom_token_count, microphone_enabled, model_id
    while True:
        display_title()
        print(f"\n")
        print(f"    1. Game Used: {game}\n")
        print(f"    2. Microphone On: {'True' if microphone_enabled else 'False'}\n")
        print(f"    3. Optimization: {optimization}\n")
        print(f"    4. Token Count: {custom_token_count}\n")
        print(f"")
        print("-" * 119)
        game_key = game.lower().replace(" ", "")
        print(f"\n")
        print(f"    model = {model_id}\n")
        print(f"    {game}_folder = {game_folders.get(game_key, 'Not set')}\n")
        print(f"    xvasynth_folder = {xvasynth_folder}")
        print(f"\n\n")
        print("=" * 119)

        choice = input("Selection, Program Options = 1-4, Refresh Display = R, Begin Mantella/xVASynth/Fallout4 = B, Exit and Save = X: ").strip().upper()
        
        if choice == '1':
            games = ["Skyrim", "SkyrimVR", "Fallout4", "Fallout4VR"]
            game = games[(games.index(game) + 1) % len(games)]
        elif choice == '2':
            microphone_enabled = not microphone_enabled
        elif choice == '3':
            optimizations = list(optimization_presets.keys())
            optimization = optimizations[(optimizations.index(optimization) + 1) % len(optimizations)]
        elif choice == '4':
            context_lengths = [2048, 4096, 8192]
            custom_token_count = context_lengths[(context_lengths.index(custom_token_count) + 1) % len(context_lengths)]
        elif choice == 'R':
            server_choice = read_temp_file()
            if server_choice == "lmstudio":
                fetch_model_details_lmstudio()
            elif server_choice == "ollama":
                fetch_model_details_ollama()
            continue
        elif choice == 'B':
            display_title()
            write_config()
            verbose_print("Saved File: config.ini")
            write_output_file(0)
            verbose_print("Saved File: .\data\temporary_batch.txt")
            verbose_print("Exiting, then Running Mantella/xVASynth...")
            return 0, xvasynth_folder
        elif choice == 'X':
            display_title()
            write_config()
            verbose_print("Saved File: config.ini")
            write_output_file(1)
            verbose_print("Saved File: .\data\temporary_batch.txt")
            verbose_print("Exiting Launcher/Optimizer...") 
            return 1, xvasynth_folder
        else:
            verbose_print("Invalid selection. Please try again.")
        
        delay()

def main():
    verbose_print("Entering main function")
    try:
        clean_config()
        check_and_update_prompts()
        read_config()

        server_choice = read_temp_file()
        if server_choice == "lmstudio":
            fetch_model_details_lmstudio()
        elif server_choice == "ollama":
            fetch_model_details_ollama()
        else:
            verbose_print("No valid model server choice found.")
            model_id = "No valid server choice"

        return display_menu_and_handle_input()
    except Exception as e:
        verbose_print(f"An unexpected error occurred: {str(e)}")
        verbose_print("Traceback:")
        verbose_print(traceback.format_exc())
        write_output_file(1)
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
    sys.exit(0)  # Always exit with code 0 to prevent the NameError
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    