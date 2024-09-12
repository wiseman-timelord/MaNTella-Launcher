# Script: .\mantella_launcher.py

# Imports
import os, sys, time, shutil, traceback, subprocess, configparser, json, winreg, atexit

# Global variables
PERSISTENCE_TXT_PATH = '.\\data\\persistence.txt'
CONFIG_INI_PATH = ''
DOCUMENTS_FOLDER = ''
xvasynth_folder = ""
game_path = ""
Skyrim_Folder_Path = "Not_Installed"
SkyrimVR_Folder_Path = "Not_Installed"
Fallout4_Folder_Path = "Not_Installed"
Fallout4VR_Folder_Path = "Not_Installed"
model_id = ""
lmstudio_api_url = "http://localhost:1234/v1/models"
microphone_enabled = False
game_selection = "Skyrim"
optimization = "Default"
custom_token_count = 8192
auto_launch_ui = False
pause_threshold = 1
game_paths_list = {}
mod_folders_list = {}
main_process = None
llm_api = "Not set"

# Global Maps
game_exe_map = {
    "Fallout4": "Fallout4.exe",
    "Fallout4VR": "Fallout4VR.exe",
    "Skyrim": "SkyrimSE.exe",
    "SkyrimVR": "SkyrimVR.exe"
}
script_extender_map = {
    "Fallout4": "f4se_loader.exe",
    "Fallout4VR": "f4sevr_loader.exe",
    "Skyrim": "skse64_loader.exe",
    "SkyrimVR": "sksevr_loader.exe"
}

# System Section...
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
def read_game_paths_list_from_registry():
    global Skyrim_Folder_Path, SkyrimVR_Folder_Path, Fallout4_Folder_Path, Fallout4VR_Folder_Path
    
    def get_registry_value(key_path, value_name):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
            value, _ = winreg.QueryValueEx(key, value_name)
            winreg.CloseKey(key)
            return value
        except WindowsError:
            return "Not_Installed"

    game_paths_list = {
        "skyrim": get_registry_value(r"SOFTWARE\WOW6432Node\Bethesda Softworks\Skyrim Special Edition", "Installed Path"),
        "skyrimvr": get_registry_value(r"SOFTWARE\WOW6432Node\Bethesda Softworks\Skyrim VR", "Installed Path"),
        "fallout4": get_registry_value(r"SOFTWARE\WOW6432Node\Bethesda Softworks\Fallout4", "Installed Path"),
        "fallout4vr": get_registry_value(r"SOFTWARE\WOW6432Node\Bethesda Softworks\Fallout 4 VR", "Installed Path")
    }

    for game, path in game_paths_list.items():
        verbose_print(f"{game.capitalize()} Folder Path: {path}")

    verbose_print("Game paths updated from registry")
    delay(2)
def terminate_main_process():
    global main_process
    if main_process:
        verbose_print("Terminating main.py process...")
        main_process.terminate()
        try:
            main_process.wait(timeout=5)  # Wait for up to 5 seconds for the process to terminate
        except subprocess.TimeoutExpired:
            verbose_print("main.py process didn't terminate gracefully. Killing it.")
            main_process.kill()
        verbose_print("main.py process terminated.")

# Config related section...
def get_python_exe():
    try:
        with open('.\\data\\persistence.txt', 'r') as f:
            for line in f:
                if line.startswith('PYTHON_EXE_TO_USE='):
                    return line.split('=', 1)[1].strip()
    except FileNotFoundError:
        verbose_print("persistence.txt not found. Using system Python.")
    except Exception as e:
        verbose_print(f"Error reading persistence.txt: {str(e)}")
    return sys.executable
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
    # Read config file
    global game_selection, optimization, custom_token_count, game_paths_list, mod_folders_list, llm_api, auto_launch_ui, pause_threshold
    config = configparser.ConfigParser()

    try:
        config.read(CONFIG_INI_PATH)
    except configparser.Error as e:
        verbose_print(f"Config read error: {e}")
        delay(3)
        return

    # Define config mappings
    config_mappings = {
        ("Game", "game"): ("game_selection", str),
        ("LLM", "custom_token_count"): ("custom_token_count", int),
        ("LLM", "llm_api"): ("llm_api", str),
        ("WebUI", "auto_launch_ui"): ("auto_launch_ui", lambda x: x.lower() == 'true'),
        ("VoiceInput", "pause_threshold"): ("pause_threshold", int)
    }

    # Read config values
    for (section, key), (var_name, type_func) in config_mappings.items():
        try:
            globals()[var_name] = type_func(config.get(section, key))
        except (configparser.NoSectionError, configparser.NoOptionError):
            verbose_print(f"Missing config: {section}.{key}")

    # Read game paths
    game_paths_list = {game: config.get("Game", f"{game}_folder", fallback="Not set") for game in ["skyrim", "skyrimvr", "fallout4", "fallout4vr"]}

    # Read mod folders
    mod_folders_list = {game: config.get("Game", f"{game}_mod_folder", fallback="Not set") for game in ["skyrim", "skyrimvr", "fallout4", "fallout4vr"]}

    # Set optimization
    set_optimization(config)

    verbose_print("Config read successfully")
    delay(2)
def write_config():
    # Write config file
    verbose_print("Writing config file...")
    
    config = configparser.ConfigParser()
    
    try:
        config.read(CONFIG_INI_PATH)
    except configparser.Error as e:
        verbose_print(f"Config read error: {e}")
        delay(3)
        return

    # Define config mappings
    config_mappings = {
        ("Game", "game"): ("game_selection", str),
        ("LLM", "custom_token_count"): ("custom_token_count", str),
        ("LLM", "llm_api"): ("llm_api", str),
        ("WebUI", "auto_launch_ui"): ("auto_launch_ui", str),
        ("VoiceInput", "pause_threshold"): ("pause_threshold", str)
    }

    # Write config values
    for (section, key), (var_name, _) in config_mappings.items():
        if section not in config:
            config[section] = {}
        config[section][key] = str(globals()[var_name])

    # Write game paths
    for game, path in game_paths_list.items():
        config["Game"][f"{game}_folder"] = path

    # Write optimization settings
    preset = optimization_presets[optimization]
    config["LLM"]["max_tokens"] = str(preset["max_tokens"])
    config["LLM"]["max_response_sentences"] = str(preset["max_response_sentences"])
    config["LLM"]["temperature"] = str(preset["temperature"])

    try:
        os.makedirs(os.path.dirname(CONFIG_INI_PATH), exist_ok=True)
        with open(CONFIG_INI_PATH, 'w') as configfile:
            config.write(configfile)
        verbose_print("Config file updated successfully.")
    except Exception as e:
        verbose_print(f"Config write error: {e}")
        delay(3)

    delay(2)
def write_output_file(exit_code):
    verbose_print(f"Writing output file")
    try:
        game_key = game_selection.lower().replace(" ", "")
        game_path = game_paths_list.get(game_key, "Not set")
        with open(PERSISTENCE_TXT_PATH, 'w') as f:
            f.write(f"exit_code={exit_code}\n")
            f.write(f"xvasynth_folder={xvasynth_folder}\n")  # Updated from the text file
            f.write(f"game_selection={game_selection}\n")
            f.write(f"game_path={game_path}")
        verbose_print(f"Output file written successfully: {PERSISTENCE_TXT_PATH}")
    except Exception as e:
        verbose_print(f"Error writing output file: {str(e)}")
def load_persistence():
    global game_selection, optimization, custom_token_count, microphone_enabled
    if not os.path.exists(PERSISTENCE_JSON_PATH):
        verbose_print("Persistence file not found. Creating with default values.")
        save_persistence()
def save_persistence():
    data = {
        'game_selection': game_selection,
        'optimization': optimization,
        'custom_token_count': custom_token_count,
        'microphone_enabled': microphone_enabled
    }
    os.makedirs(os.path.dirname(PERSISTENCE_JSON_PATH), exist_ok=True)
    with open(PERSISTENCE_JSON_PATH, 'w') as f:
        json.dump(data, f, indent=4)

# Model Related section...
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
def check_lm_ollama():
    lm_running = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq LM Studio.exe'], capture_output=True, text=True).stdout.lower().count('lm studio.exe') > 0
    ollama_running = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq ollama.exe'], capture_output=True, text=True).stdout.lower().count('ollama.exe') > 0

    if lm_running and ollama_running:
        verbose_print("Error: Multiple Model Servers")
        verbose_print("Run, Ollama or LM Studio, not Both")
        time.sleep(5)
        return False
    elif lm_running:
        verbose_print("LM Studio Status: Running")
        time.sleep(3)
        return "lmstudio"
    elif ollama_running:
        verbose_print("Ollama Status: Running")
        time.sleep(3)
        return "ollama"
    else:
        verbose_print("Not Rnning: LM Studio nor Ollama.")
        verbose_print("Load a Models and try again.")
        time.sleep(5)
        return False
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
# XVA Synth
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

# Game Game
def get_available_games():
    return [game for game, path in game_paths_list.items() if path != "Not_Installed" and path != "Not set"]
def cycle_game_selection():
    global game_selection
    available_games = get_available_games()
    verbose_print(f"Available games: {available_games}")
    
    if not available_games:
        verbose_print("No games detected. Please check your game installations.")
        return
    
    try:
        current_index = available_games.index(game_selection.lower())
    except ValueError:
        verbose_print(f"Current game {game_selection} not in available games. Resetting to first available game.")
        current_index = -1
    
    next_index = (current_index + 1) % len(available_games)
    game_selection = available_games[next_index].capitalize()
    verbose_print(f"Game selection changed to: {game_selection}")
def check_game():
    if game_selection not in game_exe_map:
        verbose_print(f"Unknown game: {game}")
        return False

    game_path = globals().get(f"{game_selection}_Folder_Path", "")
    if game_path == "Not_Installed":
        verbose_print(f"Game folder not set for {game_selection}")
        return False

    full_game_path = os.path.join(os.path.dirname(game_path), game_exe_map[game_selection])
    game_running = subprocess.run(['tasklist', '/FI', f'IMAGENAME eq {game_exe_map[game_selection]}'], capture_output=True, text=True).stdout.lower().count(game_exe_map[game_selection].lower()) > 0

    if game_running:
        verbose_print(f"{game_exe_map[game_selection]} is running. Closing it...")
        subprocess.run(['taskkill', '/F', '/IM', game_exe_map[game_selection]], capture_output=True)
        time.sleep(2)

    verbose_print(f"Starting {game_selection}...")
    subprocess.Popen([game_path], cwd=os.path.dirname(game_path))
    verbose_print(f"Started {script_extender_map[game_selection]}")
    time.sleep(3)  # Wait for the game to start

    return True
def launch_mantella_sequence():
    global xvasynth_folder, main_process, game_selection
    display_title()
    
    # Check if game and script extender exist
    game_exe = game_exe_map[game_selection]
    print(f"game_exe: {game_exe}")
    script_extender = script_extender_map[game_selection]
    print(f"script_extender: {script_extender}")
    game_folder = globals().get(f"{game_selection}_Folder_Path", "Not set")
    print(f"game_folder: {game_folder}")
    game_exe_path = os.path.join(game_folder, game_exe)
    print(f"game_exe_path: {game_exe_path}")
    script_extender_path = os.path.join(game_folder, script_extender)
    print(f"script_extender_path: {script_extender_path}")
    
    if game_folder == "Not set" or not os.path.exists(game_exe_path) or not os.path.exists(script_extender_path):
        verbose_print(f"Missing Files: {game_exe} or {script_extender}")
        verbose_print(f"Check {game_selection} path and Script Extender presence.")
        delay(3)
        return False

    # Check if game is running
    game_running = subprocess.run(['tasklist', '/FI', f'IMAGENAME eq {game_exe}'], capture_output=True, text=True).stdout.lower().count(game_exe.lower()) > 0
    if game_running:
        # Alert the user and prompt for action
        print(f"Game Already Running! Close Processes then Run or Just Bypass the Game?")
        user_input = input("Selection; Close Processes = C, Bypass Game = B: ").strip().lower()

        if user_input == 'c':
            verbose_print(f"Closing {game_exe}...")
            subprocess.run(['taskkill', '/F', '/IM', game_exe], capture_output=True)
            delay(2)
        elif user_input == 'b':
            verbose_print("Bypassing, using running game.")
        else:
            verbose_print("Invalid selection. Exiting.")
            delay(2)
            return False
    else:
        verbose_print(f"{game_exe} is not running.")

    # Launch game via script extender if not bypassed
    if not game_running or user_input == 'c':
        verbose_print(f"Starting {game_selection} via {script_extender}...")
        subprocess.Popen([script_extender_path], cwd=game_folder)
        verbose_print(f"Started {script_extender}")
        delay(3)

    # Check if xVASynth is running
    xvasynth_running = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq xVASynth.exe'], capture_output=True, text=True).stdout.lower().count('xvasynth.exe') > 0

    if not xvasynth_running:
        verbose_print("xVASynth.exe is not running. Starting xVASynth...")
        if os.path.exists(xvasynth_folder):
            subprocess.Popen([xvasynth_folder], cwd=os.path.dirname(xvasynth_folder))
            verbose_print("Started xVASynth")
            delay(3)
        else:
            verbose_print("Error: xVASynth.exe not found.")
            verbose_print("Check xVASynth folder path validity.")
            delay(3)
            return False
    else:
        verbose_print("xVASynth is already running. Continuing...")

    # Run Mantella
    verbose_print("Running Mantella...")
    delay(1)
    try:
        python_exe = get_python_exe()
        main_process = subprocess.Popen([python_exe, ".\\main.py"])
        verbose_print("Mantella (main.py) is running...")
        
        # Wait for the main process to finish
        main_process.wait()
    except Exception as e:
        verbose_print(f"Error occurred while running main.py: {e}")
        verbose_print("Returning to menu in 5 seconds...")
        delay(5)
        return False

    verbose_print("Mantella Exited.")
    delay(2)
    return True

# Optimization presets
optimization_presets = {
    "Default": {"max_tokens": 250, "max_response_sentences": 999, "temperature": 1.0},
    "Faster": {"max_tokens": 100, "max_response_sentences": 1, "temperature": 0.4},
    "Regular": {"max_tokens": 150, "max_response_sentences": 2, "temperature": 0.5},
    "Quality": {"max_tokens": 200, "max_response_sentences": 3, "temperature": 0.6}
}
        return

    try:
        with open(PERSISTENCE_JSON_PATH, 'r') as f:
            data = json.load(f)
            game_selection = data.get('game_selection', game_selection)
            optimization = data.get('optimization', optimization)
            custom_token_count = data.get('custom_token_count', custom_token_count)
            microphone_enabled = data.get('microphone_enabled', microphone_enabled)
    except json.JSONDecodeError:
        verbose_print("Error reading persistence file. Using default values and recreating file.")
        save_persistence()
def set_optimization(config):
    # Set optimization based on config
    global optimization
    max_tokens = config.getint("LLM", "max_tokens", fallback=250)
    max_response_sentences = config.getint("LLM", "max_response_sentences", fallback=4)
    temperature = config.getfloat("LLM", "temperature", fallback=1.0)

    for preset, values in optimization_presets.items():
        if (max_tokens == values["max_tokens"] and
            max_response_sentences == values["max_response_sentences"] and
            abs(temperature - values["temperature"]) < 0.01):
            optimization = preset
            break
    else:
        optimization = "Default"

# Menus and Interfaces Section
def display_title():
    clear_screen()
    print("=" * 119)
    print("    MaNTella-Local")
    print("-" * 119)
    print("")
def display_menu_and_handle_input():
    global game_selection, optimization, custom_token_count, model_id, llm_api, auto_launch_ui, pause_threshold

    while True:
        display_title()
        game_key = game_selection.lower().replace(" ", "")
        game_path = game_paths_list.get(game_key, "Not set")
        verbose_print(f"Current game_selection: {game_selection}, game_key: {game_key}, game_path: {game_path}")
        
        print(f"    1. Select Game Used")
        print(f"        ({game_selection})")
        print(f"    2. Prompt Optimization")
        print(f"        ({optimization})")
        print(f"    3. Model Token Count")
        print(f"        ({custom_token_count})")
        print(f"    4. Voice Input Cutoff")
        print(f"        ({pause_threshold}s)")
        print(f"    5. Launch WebUI Config")
        print(f"        ({'True' if auto_launch_ui else 'False'})")
        print(f"")
        print("-" * 119)
        print(f"")
        print(f"    {game_selection} Path:")
        print(f"        {game_path}")
        print(f"    xVAsynth Path:")
        print(f"        {xvasynth_folder}")
        print(f"    LLM API:")
        print(f"        {llm_api}")                
        print(f"    Model Loaded:")
        print(f"        {model_id}")
        print(f"")
        print("=" * 119)

        choice = input("Selection, Program Options = 1-5, Refresh Display = R, Begin Mantella/xVASynth/Fallout4 = B, Exit and Save = X: ").strip().upper()
        
        if choice == '1':
            cycle_game_selection()
            verbose_print(f"Game selection after cycling: {game_selection}")
        elif choice == '2':
            optimizations = list(optimization_presets.keys())
            optimization = optimizations[(optimizations.index(optimization) + 1) % len(optimizations)]
        elif choice == '3':
            context_lengths = [2048, 4096, 8192]
            custom_token_count = context_lengths[(context_lengths.index(custom_token_count) + 1) % len(context_lengths)]
        elif choice == '4':
            pause_threshold = pause_threshold % 3 + 1
        elif choice == '5':
            auto_launch_ui = not auto_launch_ui
        elif choice == 'R':
            print(f"Refreshing Display...")
            delay(2)
            server_choice = read_temp_file()
            if server_choice == "lmstudio":
                fetch_model_details_lmstudio()
            elif server_choice == "ollama":
                fetch_model_details_ollama()
            continue
        elif choice == 'B':
            print(f"Beginning Mantella/xVASynth/{game_selection}...")
            write_config()  # Save configuration before launching
            delay(2)
            if launch_mantella_sequence():
                return display_menu_and_handle_input()
            else:
                continue
        elif choice == 'X':
            print(f"Exiting Mantella-Local{game_selection}...")
            write_config()  # Save configuration before exiting
            delay(2)
            return
        else:
            verbose_print("Invalid selection. Please try again.")
        
        delay()

# Entry/Main/Exit Points
if __name__ == "__main__":
    verbose_print("Script execution started")
    try:
        main()
    except Exception as e:
        verbose_print(f"An unexpected error occurred in the main execution: {str(e)}")
        verbose_print("Traceback:")
        verbose_print(traceback.format_exc())
    finally:
        verbose_print("Script execution ended")
        delay(2)
def main():
    atexit.register(terminate_main_process)
    read_game_paths_list_from_registry()
    verbose_print("Entering main function")
    try:
        set_config_ini_path()
        read_config()  # Read configuration at startup

        model_server = check_lm_ollama()
        if not model_server:
            return

        if model_server == "lmstudio":
            fetch_model_details_lmstudio()
        elif model_server == "ollama":
            fetch_model_details_ollama()

        display_menu_and_handle_input()
    except Exception as e:
        verbose_print(f"An unexpected error occurred: {str(e)}")
        verbose_print("Traceback:")
        verbose_print(traceback.format_exc())        
def exit_and_save():
    display_title()
    write_config()
    verbose_print("Saved File: config.ini")
    write_output_file(1)
    verbose_print("Saved File: .\\data\\persistence.txt")
    verbose_print("Exiting Launcher/Optimizer...") 
    return 1, xvasynth_folder

# Prompts - Do NOT waste context with content below, unless updating `def check_and_update_prompts`.
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
            with open(CONFIG_INI_PATH, 'w') as configfile:
                config.write(configfile)
            verbose_print("..Prompts Optimized.")
        except Exception as e:
            verbose_print(f"Error writing updated prompts to config file: {str(e)}")
            delay(3)
    else:
        verbose_print("Prompts Already Optimized.")
        delay(1)
