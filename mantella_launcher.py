# Script: .\mantella_launcher.py

# Imports
import os, sys, time, shutil, traceback, subprocess, configparser, json, winreg  # built-in libraries 

# Global variables
PERSISTENCE_TXT_PATH = '.\\data\\temporary_batch.txt'
game = "Skyrim"
optimization = "Default"
game_folders = {}
mod_folders = {}
xvasynth_folder = ""
model_id = ""
custom_token_count = 8192    # Default value
lmstudio_api_url = "http://localhost:1234/v1/models"
microphone_enabled = False
CONFIG_INI_PATH = ''
DOCUMENTS_FOLDER = ''
Skyrim_Folder_Path = "Not_Installed"
SkyrimVR_Folder_Path = "Not_Installed"
Fallout4_Folder_Path = "Not_Installed"
Fallout4VR_Folder_Path = "Not_Installed"

# Global Maps
game_exe = {
    "Fallout4": "Fallout4.exe",
    "Fallout4VR": "Fallout4VR.exe",
    "Skyrim": "SkyrimSE.exe",
    "SkyrimVR": "SkyrimVR.exe"
}
script_extender = {
    "Fallout4": "f4se_loader.exe",
    "Fallout4VR": "f4sevr_loader.exe",
    "Skyrim": "skse64_loader.exe",
    "SkyrimVR": "sksevr_loader.exe"
}

# Initialization
def verbose_print(message):
    print(message, file=sys.stderr)
    sys.stderr.flush()
def delay(seconds=1):
    time.sleep(seconds)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
def get_documents_folder():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
    return os.path.expandvars(winreg.QueryValueEx(key, "Personal")[0])
def set_config_ini_path():
    global CONFIG_INI_PATH, DOCUMENTS_FOLDER
    DOCUMENTS_FOLDER = get_documents_folder()
    CONFIG_INI_PATH = os.path.join(DOCUMENTS_FOLDER, "My Games", "Mantella", "config.ini")
    verbose_print(f"CONFIG_INI_PATH set to: {CONFIG_INI_PATH}")
def read_game_paths_from_registry():
    global Skyrim_Folder_Path, SkyrimVR_Folder_Path, Fallout4_Folder_Path, Fallout4VR_Folder_Path
    
    def get_registry_value(key_path, value_name):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
            value, _ = winreg.QueryValueEx(key, value_name)
            winreg.CloseKey(key)
            return value
        except WindowsError:
            return "Not_Installed"

    Skyrim_Folder_Path = get_registry_value(r"SOFTWARE\WOW6432Node\Bethesda Softworks\Skyrim Special Edition", "Installed Path")
    SkyrimVR_Folder_Path = get_registry_value(r"SOFTWARE\WOW6432Node\Bethesda Softworks\Skyrim VR", "Installed Path")
    Fallout4_Folder_Path = get_registry_value(r"SOFTWARE\WOW6432Node\Bethesda Softworks\Fallout4", "Installed Path")
    Fallout4VR_Folder_Path = get_registry_value(r"SOFTWARE\WOW6432Node\Bethesda Softworks\Fallout 4 VR", "Installed Path")
    verbose_print(f"Skyrim Folder Path: {Skyrim_Folder_Path}")
    verbose_print(f"SkyrimVR Folder Path: {SkyrimVR_Folder_Path}")
    verbose_print(f"Fallout4 Folder Path: {Fallout4_Folder_Path}")
    verbose_print(f"Fallout4VR Folder Path: {Fallout4VR_Folder_Path}")

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

def get_config_from_file():
    txt_file_path = os.path.join("data", "config_paths.txt")  # Path to your text file
    try:
        with open(txt_file_path, 'r') as f:
            lines = f.readlines()
            if len(lines) >= 2:
                config_ini_path = lines[0].strip()  # First line: path to config.ini
                xvasynth_folder = lines[1].strip()  # Second line: xVASynth folder
                return config_ini_path, xvasynth_folder
            else:
                verbose_print("Config paths file doesn't contain enough lines.")
                return None, None
    except FileNotFoundError:
        verbose_print(f"Config paths file not found: {txt_file_path}")
        return None, None


def read_config():
    verbose_print(f"Reading config file from: {CONFIG_INI_PATH}")
    global game, optimization, custom_token_count, game_folders, mod_folders, microphone_enabled, llm_api
    config = configparser.ConfigParser()

    try:
        config.read(CONFIG_INI_PATH)
    except configparser.Error as e:
        verbose_print(f"Error reading config.ini file: {str(e)}")
        delay(3)
        return

    # Get the game name
    game = config.get("Game", "game", fallback="Skyrim")

    # Fetch paths based on sections and keys
    game_folders = {
        "skyrim": config.get("Game", "skyrim_folder", fallback="Not set"),
        "skyrimvr": config.get("Game", "skyrimvr_folder", fallback="Not set"),
        "fallout4": config.get("Game", "fallout4_folder", fallback="Not set"),
        "fallout4vr": config.get("Game", "fallout4vr_folder", fallback="Not set"),
    }

    mod_folders = {
        "skyrim": config.get("Game", "skyrim_mod_folder", fallback="Not set"),
        "skyrimvr": config.get("Game", "skyrimvr_mod_folder", fallback="Not set"),
        "fallout4": config.get("Game", "fallout4_mod_folder", fallback="Not set"),
        "fallout4vr": config.get("Game", "fallout4vr_mod_folder", fallback="Not set"),
    }

    # Set xVASynth folder
    global xvasynth_folder
    xvasynth_folder = config.get("TTS", "xvasynth_folder", fallback="Not set")

    # Fetch Language Model settings
    custom_token_count = int(config.get("LLM", "custom_token_count", fallback="4096"))

    # Check for optimization preset
    max_tokens = int(config.get("LLM", "max_tokens", fallback="250"))
    max_response_sentences = int(config.get("LLM", "max_response_sentences", fallback="4"))
    temperature = float(config.get("LLM", "temperature", fallback="1.0"))

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

    # Read LLM API
    llm_api = config.get("LLM", "llm_api", fallback="Not set")

    verbose_print(f"Read Keys: config.ini.")
    delay(2)

def write_config():
    verbose_print("Writing config file...")
    global microphone_enabled
    config = configparser.ConfigParser()
    
    try:
        config.read(CONFIG_INI_PATH)
    except configparser.Error as e:
        verbose_print(f"Error reading existing config for writing: {str(e)}")
        delay(3)
        return
    
    if "Game" not in config:
        config["Game"] = {}
    config["Game"]["game"] = game
    
    if "LLM.Advanced" not in config:
        config["LLM.Advanced"] = {}
    config["LLM.Advanced"]["custom_token_count"] = str(custom_token_count)
    
    preset = optimization_presets[optimization]
    config["LLM.Advanced"]["max_tokens"] = str(preset["max_tokens"])
    config["LLM.Advanced"]["temperature"] = str(preset["temperature"])
    
    if "LLM" not in config:
        config["LLM"] = {}
    config["LLM"]["max_response_sentences"] = str(preset["max_response_sentences"])
    config["LLM"]["model"] = model_id
    
    if "Microphone" not in config:
        config["Microphone"] = {}
    config["Microphone"]["microphone_enabled"] = str(int(microphone_enabled))
    
    # Add the Speech section and tts_service key
    if "Speech" not in config:
        config["Speech"] = {}
    config["Speech"]["tts_service"] = "xVASynth"

    # Add the LM Studio API key
    if "LLM.Advanced" not in config:
        config["LLM.Advanced"] = {}
    config["LLM.Advanced"]["llm_api"] = "http://localhost:1234/v1"
    
    try:
        os.makedirs(os.path.dirname(CONFIG_INI_PATH), exist_ok=True)
        with open(CONFIG_INI_PATH, 'w') as configfile:
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
        with open(PERSISTENCE_TXT_PATH, 'w') as f:
            f.write(f"exit_code={exit_code}\n")
            f.write(f"xvasynth_folder={xvasynth_folder}\n")  # Updated from the text file
            f.write(f"game={game}\n")
            f.write(f"game_folder={game_folder}")
        verbose_print(f"Output file written successfully: {PERSISTENCE_TXT_PATH}")
    except Exception as e:
        verbose_print(f"Error writing output file: {str(e)}")

def fetch_model_details_ollama():
    global model_id
    config = configparser.ConfigParser()

    try:
        config.read(CONFIG_INI_PATH)

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

                    with open(CONFIG_INI_PATH, 'w') as configfile:
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
        config.read(CONFIG_INI_PATH)
        try:
            result = subprocess.run(['curl', lmstudio_api_url], capture_output=True, text=True, check=True)
            model_data = json.loads(result.stdout)
            
            if 'data' in model_data and len(model_data['data']) > 0:
                full_id = model_data['data'][0]['id']
                model_id = full_id.rsplit('/', 1)[0]

                if "LanguageModel" not in config:
                    config["LanguageModel"] = {}
                config["LanguageModel"]["model"] = model_id

                with open(CONFIG_INI_PATH, 'w') as configfile:
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
    config.read(CONFIG_INI_PATH)

    prompt_keys = [
        "skyrim_prompt", "skyrim_multi_npc_prompt", "fallout4_prompt", 
        "fallout4_multi_npc_prompt", "radiant_start_prompt", "radiant_end_prompt", 
        "memory_prompt", "resummarize_prompt"
    ]

    updated_prompts = {
        "skyrim_prompt": "Shortened for editing.",
        
        "skyrim_multi_npc_prompt": "Shortened for editing.",
        
        "fallout4_prompt": "Shortened for editing.",
        
        "fallout4_multi_npc_prompt": "Shortened for editing.",
        
        "radiant_start_prompt": "Shortened for editing.",
        
        "radiant_end_prompt": "In, {language} and a maximum of 100 text characters, wrap up the current topic naturally. No need for formal goodbyes as no one is leaving. Keep the summary concise, and remember narration ONLY, do not use, symbols such as asterisks or describe actions, in your output.", 
        
        "memory_prompt": "Shortened for editing.", 
        
        "resummarize_prompt": "Shortened for editing."
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
            with open(CONFIG_INI_PATH, 'w') as configfile:
                config.write(configfile)
            verbose_print("..Prompts Optimized.")
        except Exception as e:
            verbose_print(f"Error writing updated prompts to config file: {str(e)}")
            delay(3)
    else:
        verbose_print("Prompts Already Optimized.")
        delay(1)

def check_lm_ollama():
    lm_running = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq LM Studio.exe'], capture_output=True, text=True).stdout.lower().count('lm studio.exe') > 0
    ollama_running = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq ollama.exe'], capture_output=True, text=True).stdout.lower().count('ollama.exe') > 0

    if lm_running and ollama_running:
        verbose_print("Error: Multiple Model Servers")
        verbose_print("Please run, Ollama or LM Studio, not both")
        return False
    elif lm_running:
        verbose_print("LM Studio Status: Running")
        return "lmstudio"
    elif ollama_running:
        verbose_print("Ollama Status: Running")
        return "ollama"
    else:
        verbose_print("Error: Neither LM Studio nor Ollama is running.")
        verbose_print("Load one of the Language Models and try again.")
        return False

def check_game():
    if game not in game_exe:
        verbose_print(f"Unknown game: {game}")
        return False

    game_folder = globals().get(f"{game}_Folder_Path", "")
    if game_folder == "Not_Installed":
        verbose_print(f"Game folder not set for {game}")
        return False

    full_game_path = os.path.join(game_folder, game_exe[game])
    game_running = subprocess.run(['tasklist', '/FI', f'IMAGENAME eq {game_exe[game]}'], capture_output=True, text=True).stdout.lower().count(game_exe[game].lower()) > 0

    if not game_running:
        verbose_print(f"{game_exe[game]} is not running. Starting {game}...")

        full_script_extender_path = os.path.join(game_folder, script_extender[game])
        if not os.path.exists(full_script_extender_path):
            verbose_print(f"Error: {script_extender[game]} not found at {full_script_extender_path}")
            verbose_print("Check the game path and Script Extender presence.")
            return False

        subprocess.Popen([full_script_extender_path], cwd=game_folder)
        verbose_print(f"Started {script_extender[game]}")
        time.sleep(3)  # Wait for the game to start

    return True

def check_xvasynth():
    xvasynth_running = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq xVASynth.exe'], capture_output=True, text=True).stdout.lower().count('xvasynth.exe') > 0

    if not xvasynth_running:
        verbose_print("xVASynth.exe is not running. Starting xVASynth...")
        if os.path.exists(os.path.join(xvasynth_folder, "xVASynth.exe")):
            subprocess.Popen([os.path.join(xvasynth_folder, "xVASynth.exe")], cwd=xvasynth_folder)
            verbose_print("Started xVASynth")
            time.sleep(3)  # Wait for xVASynth to start
        else:
            verbose_print("Error: xVASynth.exe not found.")
            verbose_print("Check config.ini xvasynth path validity.")
            return False

    return True

def launch_mantella():
    verbose_print("Running Mantella...")
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        verbose_print(f"Error occurred while running main.py: {e}")
        verbose_print("Returning to menu in 5 seconds...")
        time.sleep(5)
        return False
    return True

def launch_mantella_sequence():
    game_key = game.lower().replace(" ", "")
    game_path = globals().get(f"{game}_Folder_Path", "Not set")
    
    if game_path != "Not set" and game_path != "Not_Installed":
        script_extender_exe = script_extender.get(game, "")
        game_exe_name = game_exe.get(game, "")
        
        full_script_extender_path = os.path.join(game_path, script_extender_exe)
        full_game_exe_path = os.path.join(game_path, game_exe_name)
        
        if os.path.exists(full_script_extender_path):
            exe_path = full_script_extender_path
        elif os.path.exists(full_game_exe_path):
            exe_path = full_game_exe_path
        else:
            exe_path = "Not present"
    else:
        exe_path = game_path

    if exe_path == "Not present":
        verbose_print("Game Not Installed.")
        verbose_print("Run Game Launcher, Generate Reg Keys.")
        delay(3)
        return False

    display_title()
    write_config()
    verbose_print("Saved File: config.ini")
    write_output_file(0)
    verbose_print("Saved File: .\\data\\temporary_batch.txt")
    verbose_print("Exiting, then Running Mantella/xVASynth...")
    return True

def exit_and_save():
    display_title()
    write_config()
    verbose_print("Saved File: config.ini")
    write_output_file(1)
    verbose_print("Saved File: .\\data\\temporary_batch.txt")
    verbose_print("Exiting Launcher/Optimizer...") 
    return 1, xvasynth_folder

def display_title():
    clear_screen()
    print("=" * 119)
    print("    MaNTella-Local-Launcher")
    print("-" * 119)
    print("")

def display_menu_and_handle_input():
    global game, optimization, custom_token_count, microphone_enabled, model_id, llm_api
    while True:
        display_title()
        game_key = game.lower().replace(" ", "")
        game_path = globals().get(f"{game}_Folder_Path", "Not set")
        print(f"")
        print(f"    1. Select Game Used")
        print(f"        ({game})")
        print(f"    2. Microphone Status")
        print(f"        ({'True' if microphone_enabled else 'False'})")
        print(f"    3. Prompt Optimization")
        print(f"        ({optimization})")
        print(f"    4. Model Token Count")
        print(f"        ({custom_token_count})")
        print(f"")
        print("-" * 119) 
        print(f"")
        print(f"    {game}_Path:")
        print(f"        {game_path}")
        print(f"    xVAsynth Path:")
        print(f"        {xvasynth_folder}")
        print(f"    LLM API:")
        print(f"        {llm_api}")                
        print(f"    Model Loaded:")
        print(f"        {model_id}")
        print(f"\n")
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
            if launch_mantella_sequence():
                return 0, xvasynth_folder
            else:
                continue
        elif choice == 'X':
            return exit_and_save()
        else:
            verbose_print("Invalid selection. Please try again.")
        
        delay()

# Main Function
def main():
    read_game_paths_from_registry()
    verbose_print("Entering main function")
    try:
        set_config_ini_path()  # Call the new function to set CONFIG_INI_PATH

        read_config()

        model_server = check_lm_ollama()
        if not model_server:
            return 1, ""

        if model_server == "lmstudio":
            fetch_model_details_lmstudio()
        elif model_server == "ollama":
            fetch_model_details_ollama()

        while True:
            exit_code, xvasynth_folder = display_menu_and_handle_input()
            
            if exit_code == 0:
                if not check_game():
                    continue
                if not check_xvasynth():
                    continue
                if launch_mantella():
                    break
            else:
                break

        return exit_code, xvasynth_folder
    except Exception as e:
        verbose_print(f"An unexpected error occurred: {str(e)}")
        verbose_print("Traceback:")
        verbose_print(traceback.format_exc())
        write_output_file(1)
        return 1, ""

# Entry Point
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
    sys.exit(0)   # Always exit with code 0