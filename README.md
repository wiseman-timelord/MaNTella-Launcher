# Mantella-WT - the Mantella/xVASynth Optimizer-Launcher.
This is a experimental pre-release fork of [Mantella 11.4](https://github.com/art-from-the-machine/Mantella/releases/tag/v0.11.4), but for info regarding the original go [here](https://github.com/art-from-the-machine/Mantella).

# Status
 When I have integrated the optimizations from the txt file into a pre-launch menu, then there will be release, until then you can gamble on the current files, or download the launch improver pre-release. 

# Description
Drop-in files for Local-Optimization and Launching on Mantella. The Mantella xVASynth Optimizer/Launcher is a command-line tool designed to automate and optimize the workflow for managing audio generation in Skyrim and Fallout 4 using the xVASynth software. The script facilitates game configuration management, launches xVASynth if it is not already running, and performs various tasks such as cleaning configuration files and setting optimization presets for audio processing. The Python component of the script handles reading and writing configuration settings, displays an interactive menu for user selection of game and optimization options, and saves the chosen settings for subsequent executions.

# Features
These features combine to provide a comprehensive and user-friendly tool for optimizing and managing audio generation for Skyrim and Fallout 4 using xVASynth and Mantella.
1. **Batch Launcher for Automation**  
   - The script includes a batch launcher that automates the execution of both xVASynth and Mantella.
   - If xVASynth is installed in the recommended directory (`.\xVASynth`), the script will automatically launch it as needed.
   - Ensures the launcher runs with administrative privileges, facilitating seamless execution of both applications.
2. **Standardized Character Details**  
   - Processes and standardizes character details, which were previously non-standardized and often contained excessive information.
   - Enhances clarity and consistency, allowing for more effective use of character data in audio generation.
3. **Optimized Configuration Management**  
   - Optimizes and streamlines prompts for managing `config.ini`, ensuring concise and clear configuration of settings.
   - Implements character limits on specific configuration fields for consistency and ease of use.
   - Removes non-functional options such as "follow," "offended," and "forgiven" from the configuration prompts to enhance functionality and usability based on testing with the vanilla game.
4. **Interactive Python Script**  
   - The Python script handles the cleaning and reading of the configuration file, ensuring it is free from clutter and formatted correctly.
   - Provides an interactive menu for users to toggle between different games (Skyrim, SkyrimVR, Fallout4, Fallout4VR) and optimization presets (Default, Faster, Medium, Quality).
   - Allows users to adjust context length settings, offering predefined options for efficient customization.
5. **Error Handling and Logging**  
   - Includes robust error handling and logging to track the execution flow and capture any issues that arise during script execution.
   - Creates backups of the configuration file before making changes, ensuring that the original settings can be restored if needed.
6. **Automatic Execution and Exit Handling**  
   - Automatically runs Mantella after configuring xVASynth, streamlining the workflow for users.
   - Handles exit codes and saves them to an output file, ensuring proper closure and communication between the batch and Python scripts.

# Preview
- The menu of much optimization, landing today...
```
========================================================================================================================
                                        Mantella xVASynth, Optimizer / Launcher
------------------------------------------------------------------------------------------------------------------------




                                               1. Game Used: Fallout4

                                               2. Optimization: Medium

                                               3. Context Length: 4096





------------------------------------------------------------------------------------------------------------------------



                                   Fallout4_folder = D:\GamesVR\Fallout4_163
                                   Fallout4_mod_folder = D:\GamesVR\Fallout4_163\Data
                                   xvasynth_folder = D:\GamesVR\xVASynth


------------------------------------------------------------------------------------------------------------------------
Selection, Run Mantella/xVASynth = R, Program Options 1-3, Exit and Save = X:

```
- The general running of things...
```
=======================================================================================================================
                                          Mantella-xVASynth Optimizer/Launcher
------------------------------------------------------------------------------------------------------------------------

Working Dir: D:\GamesVR\Mantella-WT-0.11.3
Running Mantella xVASynth Optimizer...
Script started
Working Folder: D:\GamesVR\Mantella-WT-0.11.3
Config File: D:\GamesVR\Mantella-WT-0.11.3\config.ini
Script execution started
Entering main function
Starting config cleaning...
Found 0 comment lines.
Config Already Clean.
Checking Prompts
Prompts Alrady Optimized.
Reading config file...
Read Keys: config.ini.






```

## Requirements
1. **Python Environment**:
   - **Version**: Python 3.11 is required. Note that the script is incompatible with Python 3.12.
   - **Dependencies**: Install all necessary Python dependencies as specified in the Mantella Main requirements file. Follow any additional off-site procedures outlined in Mantella documentation for environment setup.
2. **Language Model**:
   - **Recommendation**: A suitable language model is needed for optimal text processing. It is advised to use the [Lewdiculous L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix](https://huggingface.co/Lewdiculous/L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix) model from Hugging Face. It supports both SFW and NSFW content.
3. **Operating System**:
   - **Compatibility**: The script runs on Windows 7 through Windows 11. As the Mantella-WT relies on batch files, it should work on all these versions, provided Mantella is compatible with them.
   - **Permissions**: Administrative privileges might be necessary, as certain operations require elevated permissions.
4. **xVASynth Installation**:
   - Ensure xVASynth is installed and configured properly, with the executable located in the directory specified within the `config.ini` file.
5. **Configuration File**:
   - A `config.ini` file must be present, containing sections for `Game`, `Paths`, and `LanguageModel.Advanced`. This file is used to set paths and audio optimization parameters for *Skyrim* and *Fallout 4*.
6. **Dependencies**:
   - The script uses Python standard library modules such as `configparser`, `os`, `sys`, `time`, `shutil`, and `traceback`.

# Usage / Install
1. Ensure the Mantella mod is installed for Fallout/Skyrim from the Nexus mods site, follow the guide, this will, at some point, require install [Mantella 11.4](https://github.com/art-from-the-machine/Mantella/releases/tag/v0.11.4) to a suitable directory.
2. After completing Mantella install, then download the [Latest working Mantella-WT release](https://github.com/wiseman-timelord/Mantella-WT/releases/), drop the files into the main Mantella folder, preserving folders.
4. Ensure you have LM Studio / ollama loaded and configured and serving, offload a suitable number of layers to the GPU if Game is on same card, ensure the api addresses are correctly configured.
5. Configure the ".\config.ini", ensure you have entered things like, "fallout4_folder" and "fallout4_mod_folder" and "llm_api" and "model" and "tts_service".
6. Run Fallout 4/Skyrim, and then run the `Mantella-WT.Bat` batch, the "config.ini" will be cleaned/backup, and then you will be presented with the menu.
- Hopefully you have, Admin rights and sensible system settings, but click allow on firewall as required, I am guessing its the interaction between Mantella and the Mantella Mod.

## Notes
- all options for Optimization are shown...
```
Default
max_tokens = 250
max_response_sentences = 999
temperature = 1

Faster
max_tokens = 100
max_response_sentences = 1
temperature = 0.4

Medium
max_tokens = 150
max_response_sentences = 2
temperature = 0.5

Quality
max_tokens = 200
max_response_sentences = 3
temperature = 0.6
```


- Noticing the improvements in Language models, 1 token per word? it used to be 5 tokens for every 4 letters, and 4 tokens for every 3 tokens, or something was the calculation, when we were at llama 1 stage, if I am not hallucinating, this is highly impressive advancements, but requires re-assessment of what is a "Required number of Tokens".
- a Llama 3 Q3_m model with fallout 4 dlc & ~300 mods including 512 wasteland texture pack, utilizes all of the 8GB on a single card, if you want to use =>Q4, then I suggest 12GB Gpu. Need to try the PhyOp Reduced.


# Development
- after make launcher/optimizer, then work on more files, to streamline them for local only was part of the original idea, but, I should keep that feature. So, updates for dropin replacement files, to upgrade and streamline current scripts, then demonstrate/push them to main, before altering stuff radically. 
- Possibly requires advance of my project for utilizing llama.cpp pre-compiled binaries for vulkan, to host models with OhLlama/LmStudio compatibility for apps, as they are not utilizing threads properly or vulkan at all, currently.
- tuned towards local models, scripts will be streamlined, people whom use online can still use the launcher, but not the dropin files. 
- NExt version is "Mantella-WT v0.11.3.1".
- Next version will also read the "xvasynth_folder" so as to not require the xVASynth to be installed in `.\xVASynth`, it accesses the config.ini.
- The updated prompts and q3_m model seem to be able to ignore the lines starting "*", and not print out lines with "*". These prompts should be optionally injected into the config.ini, so as to not require the config_ini_updates.txt file manual modification.
- The config.ini model name value should be obtained through the curl through "llm_api" key with the api, example "llm_api = http://localhost:1234/v1", in the python script to read this, then ensure this is also written to the "model" key in "config.ini", for example...
```
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{ 
    "model": "Lewdiculous/L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix",
    "messages": [ 
      { "role": "system", "content": "Always answer in rhymes." },
      { "role": "user", "content": "Introduce yourself." }
    ], 
    "temperature": 0.7, 
    "max_tokens": -1,
    "stream": true
}'
```
...would result in saving...
```
model = Lewdiculous/L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix
```
...and the menu would also be displaying it after it has been read, like the other ones...
```



           model = Lewdiculous/L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix
           fallout4_folder = D:\GamesVR\Fallout4_163
            fallout4_mod_folder = D:\GamesVR\Fallout4_163
             xvasynth_folder = D:\GamesVR\Mantella-WT-0.11.4\xVASynth


                       
```
...the menu should then have options for...
```
Selection, Program Options = 1-3, Refresh Display = R, Begin Mantella/xVASynth = B, Exit and Save = X:
```
...hence when it refreshes, it will need to read the values of the curl again, because logically the user would have changed the model, dont worry about re-reading the config.
- it should only create a backup file, if "config.bak" is not present already, the idea is the original version will have comments, that explain what the different parts mean, and what the options are, this way the user has a reference config. So it needs to check for this, and if it exists, then just continue to save the config.ini, if not back the config.ini up, if the batch detects there is no config.bak, then before processing "config.bak", it should also run "pip install -r requirements.txt".
- if there are no lines that start with comments ";" in the "config.ini", then it will not require cleaning, its only if the commented lines are there, then it should do the cleaning, but also do the blank lines, and spacing above the titles, as it does, apart from in the top line, which should be a title. At the moment, it is checking for blank lines, but the blank lines are the ones above the titles, which it removes, then puts back in, which is un-neccessary, and could end up corrupting the config.ini with all the unneccessary parsing and saving, just for it to be the same as the already processed version it just opened.
- Dynamic switching between, prompt sets and for differing context, depending upon the maximum context for the model, we could switch between ONLY 4096, 8192, in the mantella scripts, depending upon the value of "custom_token_count", I want 2 versions of the characters.csv details, one should have 1 sentence description, the other 2, so as to use the better one for the higher context. 
- Need to remove warning, and streamline code for context assessment, and use the setting from the config.ini, then user can toggle the context lengths from the menu.
- "tts_service" will always be "tts_service = xVASynth", the python script should ensure this when saving.
-  main-wt.txt should be deleted after the batch has used it.
- Option on menu for the key "microphone_enabled", true/false, this will relate to 0, 1, for example... "microphone_enabled = 1", this choice will also require, loading and displaying as another toggle option, and saving when the config.ini is saved on run or exit. 
- if upon run, the batch does not detect the presence of "config.bak", then it should run "pip install -r requirements.txt", so as to be foolproof.

# Disclaimer
- This is a fork by Wiseman-Timelord, meaning, if you have issues with the program, its Likely not my code, you would have to check that.
- My forks sometimes just up and dissapear, this tends to happen when I no longer use the relating program, to neaten up things a little.
