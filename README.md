# Mantella-WT - the Mantella/xVASynth Optimizer-Launcher.
Status: Working, further development possible.

# Description
Drop-in files for Local-Model Optimization and Launching Mantella. The Mantella xVASynth Optimizer/Launcher is a command-line tool designed to automate and optimize the workflow for managing audio generation in Skyrim and Fallout 4 using the xVASynth software. The script facilitates game configuration management, launches xVASynth if it is not already running, and performs various tasks such as cleaning configuration files and setting optimization presets for audio processing. The Python component of the script handles reading and writing configuration settings, displays an interactive menu for user selection of game and optimization options, and saves the chosen settings for subsequent executions.

# Features
1. **Batch Launcher for Automation**: Automates and runs xVASynth and Mantella with admin privileges.
2. **Standardized Character Details**: Standardizes character data for clarity and effective audio generation.
3. **Optimized Configuration Management**: Streamlines `config.ini` prompts and removes non-functional options.
4. **Interactive Python Script**: Cleans configuration files and offers an interactive menu for game and preset choices.
5. **Error Handling and Logging**: Tracks errors, logs execution, and backs up configuration files.
6. **Automatic Execution and Exit Handling**: Runs Mantella post-xVASynth and manages exit codes for smooth operation.

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
Settings saved. Proceeding to run Mantella/xVASynth...
Writing output file: exit_code=0, xvasynth_path=D:\GamesVR\xVASynth
Output file written successfully: main-wt.txt
0,D:\GamesVR\xVASynth
Final output: exit_code=0, xvasynth_path=D:\GamesVR\xVASynth
Script execution ended
...Mantella/xVASynth Optimizer-Launcher Closed...
Checking for xVASynth...
Running Mantella...
Mantella-WT for Mantella version 0.11.4
Mantella currently running for Fallout4 (D:\GamesVR\Fallout4_163).
Mantella mod located in D:\GamesVR\Fallout4_163\Data.
21:33:50.151 INFO: Running Mantella with local language model
21:33:50.152 WARNING: L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix is using token_limit of 4096
21:33:50.361 TTS: Connecting to xVASynth...
21:33:50.510 STT: Audio threshold set to 'auto'. Adjusting microphone for ambient noise...
21:33:50.510 STT: If mic input too low, edit audio_threshold value manually in .\config.ini.
Need help? See here: https://art-from-the-machine.github.io/Mantella/pages/issues_qna
Waiting for player to select an NPC for Communication...

```

## Requirements
1. **Python Environment**: Requires Python 3.11 and dependencies from the Mantella requirements file.
2. **Language Model**: Use [Lewdiculous L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix](https://huggingface.co/Lewdiculous/L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix) with Q3 or Q4 VRAM specifications.
3. **Operating System**: Compatible with Windows 7 through Windows 11; administrative privileges may be needed.
4. **xVASynth Installation**: Must be installed and correctly configured in the specified directory.
5. **Configuration File**: Requires a `config.ini` with `Game`, `Paths`, and `LanguageModel.Advanced` sections.
6. **Dependencies**: Utilizes Python standard library modules like `configparser`, `os`, `sys`, `time`, `shutil`, and `traceback`.

# Usage / Install
1. Ensure the [Mantella Mod](https://www.nexusmods.com/fallout4/mods/79747) is installed for Fallout/Skyrim from the Nexus mods site, follow the guide, this will, at some point, require install [Mantella 11.4](https://github.com/art-from-the-machine/Mantella/releases/tag/v0.11.4) to a suitable directory.
2. After completing Mantella 11.4 install, then download the [Latest working Mantella-WT release](https://github.com/wiseman-timelord/Mantella-WT/releases/), drop the files into the main Mantella folder, preserving folders.
4. Ensure you have LM Studio / ollama loaded and configured and serving, offload a suitable number of layers to the GPU if Game is on same card, ensure the api addresses are correctly configured.
5. Configure the ".\config.ini", ensure you have entered things like, "fallout4_folder" and "fallout4_mod_folder" and "llm_api" and "model" and "tts_service".
6. Run Fallout 4/Skyrim, and then run the `Mantella-WT.Bat` batch, the "config.ini" will be cleaned/backup, and then you will be presented with the menu.
- Hopefully you have, Admin rights and sensible system settings, but click allow on firewall as required, I am guessing its the interaction between Mantella and the Mantella Mod.

## Notes
- all options for Optimization are shown...
```
Default: max_tokens = 250, max_response_sentences = 999, temperature = 1
Faster: max_tokens = 100,max_response_sentences = 1, temperature = 0.4
Medium: max_tokens = 150, max_response_sentences = 2, temperature = 0.5
Quality: max_tokens = 200, max_response_sentences = 3, temperature = 0.6
```
- the "Offended" and "Forgiven", commands are removed, this is because, offended will depend on the model, and most likely on local models, asking for forgiveness would not have a result before the player is dead? So, I find these things a nice idea, but a bit naff. I would prefer commands like "Attack" and "Hold Back", to switch between, Aggressive and Cautious. Either way, it was additional weight, and I wanted the prompts to work, correctly and fast, on Q3_M Local Models.

- a Llama 3 Q3_m model with fallout 4 dlc & ~300 mods including 512 wasteland texture pack, utilizes all of the 8GB on a single card, if you want to use =>Q4, then I suggest 12GB Gpu. Need to try the PhyOp Reduced.

# Development
- Noticing the improvements in Language models, 1 token per word? it used to be 5 tokens for every 4 letters, and 4 tokens for every 3 tokens, or something was the calculation, when we were at llama 1 stage, if I am not hallucinating, this is highly impressive advancements, but requires re-assessment of what is a "Required number of Tokens".
- Possibly requires advance of my project for utilizing llama.cpp pre-compiled binaries for vulkan, to host models with OhLlama/LmStudio compatibility for apps, as they are not utilizing threads properly or vulkan at all, currently.
- tuned towards, windows and local models, scripts will be streamlined, people whom use online can still use the launcher, but not the dropin files. 
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
