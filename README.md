# Mantella-Local-Launcher for [Mantella v11.4](https://github.com/art-from-the-machine/Mantella/releases)
Status: Revisit 09/2024. Work to do, firstly a overhaul of the batches, then tackle `launcher.py`..
- (testing) Compatibility with both default python locations.
- (testing) use of `python.exe -m pip` instead of `pip.exe`.
- (testing) Optimized and improved display code.
- (testing) Use of my new, DP0 and Admin Check, block.
- Do Away with code specific to v11, config.ini will no longer be in same place, need to see where they put it in new version, and make my setup/launcher v12 only.
- Update for completion of v12 compatibility, as its now no-longer beta.

### Description
- a Windows Launcher/Optimizer for Mantella for, Fallout 4 and Skyrim, with models locally on Windows. Mantella was optimized for 8K on GPT, so, Mantella-Local-Launcher instead optimizes Mantella for Local Models. The script facilitates pre-launch, configuration management and optimization, launches, xVASynth and your chosen game, if they are not already running, then it launches Mantella, by making use of the settings already present in `config.ini`, so you do still need to configure that first. Mantella-Local-Launcher also performs various tasks such as, cleaning configuration files and optimizing the mantella prompts. The Batch file manages the, communication between and launching, of the relevant programs/scripts, while the Python component of the script handles the heavy work, and displays an interactive menu for user selection of game and optimization options. The project is local only, so, gpt/online, compatibility and optimization, remains untested. 

### Features
1. **Batch Launcher for Automation**: Automates and runs xVASynth and Mantella with admin privileges.

3. **Optimized Configuration Management**: Streamlines `config.ini` prompts and removes non-functional options.
4. **Interactive Python Script**: Cleans configuration files and offers an interactive menu for game and preset choices.
5. **Error Handling and Logging**: Tracks errors, logs execution, and backs up configuration files.
6. **Automatic Execution and Exit Handling**: If not already running, then runs, Fallout 4 and/or xVASynth, and then continues to Mantella for smooth operation.
7. **LM Studio / Ollama Support **: Switch models to similar one with different name, and it is handled by the launcher in `config.ini`.
8. **Auto-Optimize Prompts**: Prompts are upgraded/streamlined, character sheets will be optimized based on context, but that part is still being worked on.
9. **Auto-Environment Selection**: Code enables python location to be found, and correct version of python and pip to be used. 
10. **Standardized Character Details**: Standardizes character data is being worked on, it will autop optimize character details to, 1, 2, 3, 4, sentence length.

### Preview
- The menu of much simplified optimization...
```
=======================================================================================================================
                                               Mantella-Local-Launcher
-----------------------------------------------------------------------------------------------------------------------





                                               1. Game Used: Fallout4

                                               2 Microphone On: False

                                               3. Optimization: Regular

                                               4. Token Count: 4096





-----------------------------------------------------------------------------------------------------------------------

                                   model = Lewdiculous/L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix
                                   Fallout4_folder = D:\GamesVR\Fallout4_163
                                   xvasynth_folder = D:\GamesVR\xVASynth

=======================================================================================================================
Selection, Program Options = 1-4, Refresh Display = R, Begin Mantella/xVASynth = B, Exit and Save = X:

```
- The general running of things...
```
=======================================================================================================================
                                               Mantella-Local-Launcher
------------------------------------------------------------------------------------------------------------------------

Working Dir: D:\GamesVR\Mantella-WT-0.11.4
Running Mantella xVASynth Optimizer...
Script started
Working Folder: D:\GamesVR\Mantella-WT-0.11.4
Config File: D:\GamesVR\Mantella-WT-0.11.4\config.ini
Script execution started
Entering main function
Starting config cleaning...
Found 0 comment lines.
Config Already Clean.
Checking Prompts
Prompts Alrady Optimized.
Reading config file...
Read Keys: config.ini.
Writing config file...
Config file updated successfully.
Saved File: config.ini
Writing output file
Output file written successfully: temp-wt.txt
Saved File: temp-wt.txt
Exiting, then Running Mantella/xVASynth...
0,D:\GamesVR\xVASynth
Final output: exit_code=0, xvasynth_path=D:\GamesVR\xVASynth
Script execution ended
...Mantella/xVASynth Optimizer-Launcher Closed.
Read File: temp-wt.txt
Checking for Fallout4...
f4se_loader.exe is not running. Starting Fallout4...
Found and running f4se_loader.exe.
Checking for xVASynth...
xVASynth.exe is not running. Starting xVASynth...
Running Mantella...
Mantella currently running for Fallout4 (D:\GamesVR\Fallout4_163). Mantella mod located in D:\GamesVR\Fallout4_163\Data
19:55:00.415 INFO: Running Mantella with local language model
Could not find number of available tokens for L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix. Defaulting to token count of 4096 (this number can be changed via the `custom_token_count` setting in config.ini)
19:55:00.416 WARNING: Local language model has a low token count of 4096. For better NPC memories, try changing to a model with a higher token count

Mantella v0.11.4
19:55:00.623 TTS: Connecting to xVASynth...

"NPC not added. Please try again after your next response"? See here:
https://art-from-the-machine.github.io/Mantella/pages/issues_qna

Waiting for player to select an NPC...

```
- The `Setup-Install.Bat` Main Menu (upcoming version)...
```
========================================================================================================================
                                       MaNTella-Local For Mantella v11.4
========================================================================================================================









    1. Install Requirements

    2. Install Torch[CPU]

    3. Upgrade Pip Version









========================================================================================================================
Selection; Menu Options (1-3), Exit Install-Setup (X):
```

## Requirements
1. **Powerful Computer**: Running Fallout 4/Skyrim and interference on models can be intensive.
2. **Python Environment**: Requires Python 3.11 and dependencies from the Mantella requirements file.
3. **Language Model**: Use [Lewdiculous L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix](https://huggingface.co/Lewdiculous/L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix). Have, 4GB VRam Free for Q3 or 6GB VRam free for Q4. 
4. **Operating System**: Compatible with Windows 7 through Windows 11; administrative privileges may be needed.
5. **xVASynth Installation**: Must be installed and correctly configured in the specified directory.
6. **Configuration File**: Requires a `config.ini` with `Game`, `Paths`, and `LanguageModel.Advanced` sections.
7. **LM Studio or Ollama**: Obtain model folder/name and foolproofs api config, Mantella-Local-Launcer will not work on non-local model host services.

# Usage / Install
1. Ensure that Python 3.11 was installed to, the default directory or the default directory for all users.
2. Ensure the [Mantella Mod](https://www.nexusmods.com/fallout4/mods/79747) is installed for Fallout/Skyrim from the Nexus mods site, follow the guide, this will, at some point, require install [Mantella 11.4](https://github.com/art-from-the-machine/Mantella/releases/tag/v0.11.4) to a suitable directory.
3. Download the [Latest Release](https://github.com/wiseman-timelord/Mantella-Local-Launcher/releases) of the launcher, and drag the, file(S) and folder(s), from the zip into the main Mantella folder.
4. Run `1a. Install-Setup-Libraries.Bat`, this will ensure you have installed the requirements to the correct install of python. If, it exits with a torch error and/or you do not have cuda, then run `1b. Install_Torch_Cpu(Optional).bat`, so as install, "Torch+Cpu" and "TorchAudio+Cpu" and "TorchVision+Cpu, as "xVASynth" will likely have less issues. 
5. Run `2a. Mantella-Local-Launcher.Bat` for the Launcher, configure your optimizations, and when done then select "B" for begin. In future you should run `2b. Mantella_No_Launcher.Bat`, unless you wish to alter the optimizations.
  
## Notes
- all options for Optimization are shown...
```
Default: max_tokens = 250, max_response_sentences = 999, temperature = 1
Faster: max_tokens = 100, max_response_sentences = 1, temperature = 0.4
Regular: max_tokens = 150, max_response_sentences = 2, temperature = 0.5
Quality: max_tokens = 200, max_response_sentences = 3, temperature = 0.6
```
- The System Prompt on your Model Server, should be something like "You are, to requirement, an AI, role-player and text processor, you will be instructed to either be, roleplaying with the Player/NPCs."...
<img src="./media/lm_studio_prompt_mantella.jpg" align="center" alt="no image" width="313" height="315">
- If you are using one graphics card for, game and model, then ensure to use nVidia/Amd control panels to monitor free ram when fallout 4 is running, the amount of free space with small additional amount for runnings, determines what size of model you will be using.
- a Llama 3 Q3_m model with fallout 4 dlc & ~300 mods including PhyOp performance texture pack, utilizes all of the 8GB on a single card, if you want to use =>Q4 and/or hd textures, then 12GB GPU is suggested, or maybe you have heard of things like PhyOp AI Enhanced Textures.
- this project will not replace the impressive new configuration interface coming in v12, but as a result of my launcher the user will probably just use that the first time.
- No GPT/Online support! Despite loving GPT for other things, GPT will always be filtered response, despite being fast. I cant see it being used when there are local models able to produce SFW AND NSFW contents in one model and process text, I consider, Fallout4 and Skyrim, to be *Ahem* Offline Games with a little tweaking, unless you have like of achievements otherwise known as character profiling.
- There is also my mod collection specifically designed for Mantella, [MWO2 - Mantella Wasteland Operator](https://www.youtube.com/watch?v=ayZmcOqZ8iY), in that, initially the mods from MWO1 that had issues with Mantella were removed. 

# Development
- to do dynamic processing of characters.csv, to match the context length option, though for now this controls the context length saved in the config.ini file.
- For v12 compatibility, there are not the keys "fallout4_folder" and "skyrim_Folder", need to ensure the launcher understands how many keys it will be retrieving. the solution is to use similar code to what is in the batch to detect what version of mantella is running...
```
if exist ".\config.ini" (
    set "mantella_version=v11.4"
    set "config_folder=.\"
) else if exist "%USERPROFILE%\Documents\My Games\Mantella\config.ini" (
    set "mantella_version=v12"
    set "config_folder=%USERPROFILE%\Documents\My Games\Mantella"
) else (
    echo Error: File Missing: config.ini
    timeout /t 5 >nul
    goto :end_of_file
)
```
...then just dont run fallout 4 in v12, however, later on I will implement the proper way to do it would be the registry keys, this would however take extra making sures, and system backups, I dont want to have to reinstall..
- Next version is merge of Batch and Python scripts, pushin batch into the python script, its turning out complicated, but is mostly there, and optimized to 500 lines, I expect that to grow to 550-600 before everything is fixed. 
- Ensure the launcher is future proof, by having alternate method to update the relevant config prompts, this will involve acceesing the new config scripts, there are multiple look in the src folder.
- Character sheet must be backed up  "gamename_characters.bak", and then backup must be used to dynamically in relevance to the context size chosen, be filtered to contain, 2048 = 1 sentences, 4096 = 2 sentences, 8192 = 4 sentences, context lengths should be either, 2048, 4096, 8192, process the gamename_characters.csv according to the current context settings for context, and over-write any existing csv file. 
- There needs to be a Yaml ".\data\temporary_launcher.yaml", to remember the user's selection of drive for the models, then it will just use that entry from then on. 
- Now have skyrim again, and will be able to test/auto-optimize the character sheets based on context for, skyrim and fallout.
- get all of the code accurately into the python script, and compile into exe, and upload to nexus. 
3. requires re-assessment of what is a "Required number of Tokens" for llama 3 level, as noticed it was generating at 1 token per word.
4. Launcher GUI.


## Disclaimer
This software is subject to the terms in License.Txt, covering usage, distribution, and modifications. For full details on your rights and obligations, refer to License.Txt.
