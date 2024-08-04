# Mantella-WT.
This is a experimental pre-release fork of [Mantella 11.4](https://github.com/art-from-the-machine/Mantella/releases/tag/v0.11.4), For info regarding the original go [here](https://github.com/art-from-the-machine/Mantella).

# Description
Wiseman-Timelords Drop-in files for Local-Optimization and Launching on Mantella. tuned towards local models. Early stages; after make launcher/optimizer, then work on more files, to streamline them for local only, and maybe some other updates for dropin replacement files. Possibly requires advance of my project for utilizing llama.cpp pre-compiled binaries for vulkan, to host models with OhLlama/LmStudio compatibility for apps, as they are not utilizing threads properly or vulkan at all, currently. When I have integrated the optimizations from the txt file into a pre-launch menu, then there will be full release.

# Features
Work done currently includes...
1. Batch launcher, that launches BOTH, xVASynth AND Mantella, in Admin, if you install xVASynth to the suggested folder ".\xVASynth", it will, as required, automatically run it too.
2. Concise Chararacter details. The character details were non-standardized, and generally both had too much info, so I wrote a program to standardize the character details.
3. Concise, optimized and streamlined, prompts for config.ini, with stated charater limit on consolidation. follow, offended, forgiven were removed, as they didnt work in vanilla when tested.

# Preview
- The current pre-release launcher batch...
```
==============================================================================
                   Mantella xVASynth, Optimizer / Launcher
------------------------------------------------------------------------------

Maintenance for config...
Auto-Cleaning .\config.ini
- Blank lines: 0
- Commented lines: 0
Cleaning Not Required.
config.ini Location: D:\GamesVR\Mantella-0.11.4
...Maintenance Complete.

xVASynth Automation...
Checking running processes...
xVASynth.exe is already running. Continuing to Mantella...
...xVASynth Automated.

Running Mantella...
Mantella Work Dir: D:\GamesVR\Mantella-0.11.4
Mantella-WT for Mantella version 0.11.4
Mantella currently running for Fallout4 (D:\GamesVR\Fallout4_163).
Mantella mod located in D:\GamesVR\Fallout4_163\Data.
21:30:12.290 INFO: Running Mantella with local language model
21:30:12.291 WARNING: L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix is using token_limit of 4096
21:30:12.512 TTS: Connecting to xVASynth...
21:30:12.677 STT: Audio threshold set to 'auto'. Adjusting microphone for ambient noise...
21:30:12.678 STT: If mic input too low, edit audio_threshold value manually in .\config.ini.
Need help? See here: https://art-from-the-machine.github.io/Mantella/pages/issues_qna
Waiting for player to select an NPC for Communication...

```

# Usage / Install
1. Ensure the Mantella mod is installed for Fallout/Skyrim from the Nexus mods site, follow the guide, this will, at some point, require install [Mantella 11.4](https://github.com/art-from-the-machine/Mantella/releases/tag/v0.11.4) to a suitable directory.
2. After completing Mantella install, then download the [Latest working Mantella-WT release](https://github.com/wiseman-timelord/Mantella-WT/releases/), drop the files into the main Mantella folder, preserving folders.
3. Copy/Move xVASynth to `.\ExampleMantellaDirectory\xVASynth`, keeping things tidy. If you did move xVASynth, then click "Reset Paths" in the configuration.  If you do not mode xVASynth, then ensure it is run first always.
4. Ensure you have LM Studio loaded and configured, manager your GPU/CPU configurations for optimal output on your hardware, I use GPU 50-75%/CPU 25-50%, as this will be along side Fallout 4, on 8GB VRam. 
5. Ensure your model is suitable, currently I advise this model [this one from huggingface.co](https://huggingface.co/Lewdiculous/L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix),  in, q3_s, q3_m, q4_xs, q4_s. with my dropin files it will recognise the model.
6. Run the main script `python .\main.py` once, to generate the ".\config.ini" file, then close mantella, and configure the ".\config.ini" after its created. Ensure to also implement updates from `.\config_ini_updates.txt` to ".\config.ini".
7. Run Fallout 4/Skyrim, and then run the `Mantella-WT.Bat` batch, it will, as required, clean the ".\config.ini" and backup the old version to ".\config.bak", and then run "Mantella-WT".

## Notes
- The model name can be obtained through standalone python script used by batch to determine the settings being broadcasted by LM Studio or whatever model hosting, then ensure this is current in config. Determine what can simlarly be obtained, has the base folder moved, etc, auto correction.

- Noticing the improvements in Language models, 1 token per word? it used to be 5 tokens for every 4 letters, and 4 tokens for every 3 tokens, or something was the calculation, when we were at llama 1 stage, if I am not hallucinating, this is highly impressive advancements, but requires re-assessment of what is a "Required number of Tokens".
- a Llama 3 Q3_m model with fallout 4 dlc & ~300 mods including 512 wasteland texture pack, utilizes all of the 8GB on a single card, if you want to use =>Q4, then I suggest 12GB Gpu. Need to try the PhyOp Reduced.
- You need to turn off survival mode, and just use Very Hard instead, until someone produces a mod to turn off the needs messages, it confuses the AI.

# Development 
- Next version is shaping up like this...
```
==============================================================================
                   Mantella xVASynth, Optimizer / Launcher
------------------------------------------------------------------------------




                       1. Run, Mantella and xVASynth.

                       2. Game Used: Fallout4/Fallout4VR/Skyrim/SkyrimVR

                       3. Context Length: 2048/4096/8096/16384

                       4. Optimization: Default/Faster/Medium/Quality




------------------------------------------------------------------------------
Selection, Options 1-4, Exit = X:

```
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

- Development, stuck at file operations in batch, requires to check if ".data\config.ini" exists, and if not then use powershell to convert the ".\config.ini" to a ".\data\config.ini", therein, removing all, blank lines and ";Commented lines", and use the "[Titles]" for branches, and on those branches then the relevant keys with their corresponding values. Only have keys/values and branches. then save to the new file ".\data\config.ini", this is then the file we will be updating with our optimizer. 
- If still issues with read/write in batch then, might have to use python 3.11 or powershell core 7 for my main optimizer/launcher. transformation of bulk of code, so as to create new script and use batch as launcher to just run main_script.py/ps1...
- The general idea is to improve the speed of conversation, this could involve Dynamic switching between, prompt sets and for differing context, depending upon the maximum context for the model, we could work up to that, possibly we could switch between 2000, 4000, 8000, themed content, so as for less to process in appropriate situation. Potentially 3 versions of the characters .csv, 1/2/3 sentence description limit for each character. 2k context for greeting, 4k for the continuation with recent history summary or something, 8k for the rest of the convo with full convo history? First time is full context because probably wont use it all and will want best quality response, as speak to most for one or two times. possibly llm could decide based on previous answers to extend or retract, context by requesting addition of preferences for relevant things at end of prompt? Maybe A flag will be reset when convo ends, thus enabling quick interactions to begin as required. Some of the inputs, can actually be dynamic, and not present at all in user interaction, most/some of this could scale based on context size and be reasonable settings, see examples in "other notes" section.
- It reads the updates from the ini at the start, to determine the current theme of the settings. 
- Next version will also read the "xvasynth_folder" so as to not require the xVASynth to be installed in `.\xVASynth`.
- Need to remove warning, and streamline code for context assessment, and use the setting from the config.ini, then user can toggle the context lengths from the menu.

# Disclaimer
- This is a fork by Wiseman-Timelord, meaning, if you have issues with the program, its Likely not my code, you would have to check that.
- My forks sometimes just up and dissapear, this tends to happen when I no longer use the relating program, to neaten up things a little.
