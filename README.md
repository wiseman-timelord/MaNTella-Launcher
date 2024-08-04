# Mantella-WT - the Mantella/xVASynth Optimizer-Launcher.
This is a experimental pre-release fork of [Mantella 11.4](https://github.com/art-from-the-machine/Mantella/releases/tag/v0.11.4), For info regarding the original go [here](https://github.com/art-from-the-machine/Mantella).

# Description
Wiseman-Timelords Drop-in files for Local-Optimization and Launching on Mantella. tuned towards local models. Early stages; after make launcher/optimizer, then work on more files, to streamline them for local only, and maybe some other updates for dropin replacement files. Possibly requires advance of my project for utilizing llama.cpp pre-compiled binaries for vulkan, to host models with OhLlama/LmStudio compatibility for apps, as they are not utilizing threads properly or vulkan at all, currently. When I have integrated the optimizations from the txt file into a pre-launch menu, then there will be full release.

# Features
Work done currently includes...
1. Batch launcher, that launches BOTH, xVASynth AND Mantella, in Admin, if you install xVASynth to the suggested folder ".\xVASynth", it will, as required, automatically run it too.
2. Concise Chararacter details. The character details were non-standardized, and generally both had too much info, so I wrote a program to standardize the character details.
3. Concise, optimized and streamlined, prompts for config.ini, with stated charater limit on consolidation. follow, offended, forgiven were removed, as they didnt work in vanilla when tested.

# Preview
- The menu of much little configuration, landing today...
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
                                   xvasynth_folder = D:\GamesVR\Mantella-WT-0.11.4\xVASynth


------------------------------------------------------------------------------------------------------------------------
Selection, Run Mantella/xVASynth = R, Program Options 1-3, Exit and Save = X:

```
- The general running of things...
```
========================================================================================================================
                                          Mantella-xVASynth Optimizer/Launcher
------------------------------------------------------------------------------------------------------------------------

Running Mantella xVASynth Optimizer...
Script started
Working Folder: D:\GamesVR\Mantella-WT-0.11.4
Config File: D:\GamesVR\Mantella-WT-0.11.4\config.ini
Script execution started
Entering main function
Starting config cleaning process...
Found 14 blank lines and 0 comment lines.
Backup created: config.bak
Removing clutter and formatting...
Config file cleaned and saved successfully.
Reading config file...
Read Keys: config.ini.

xVASynth Automation...
Checking running processes...
xVASynth.exe is not running.
Starting xVASynth...
...xVASynth Automated.

Running Mantella...
Mantella-WT for Mantella version 0.11.4

```

# Usage / Install
1. Ensure the Mantella mod is installed for Fallout/Skyrim from the Nexus mods site, follow the guide, this will, at some point, require install [Mantella 11.4](https://github.com/art-from-the-machine/Mantella/releases/tag/v0.11.4) to a suitable directory.
2. After completing Mantella install, then download the [Latest working Mantella-WT release](https://github.com/wiseman-timelord/Mantella-WT/releases/), drop the files into the main Mantella folder, preserving folders.
4. Ensure you have LM Studio loaded and configured and serving, offload a suitable number of layers to the GPU if they are on same card, and ensure your model is suitable, I advise [this one from huggingface.co](https://huggingface.co/Lewdiculous/L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix),  in q3_m if you have ~4GB VRam Free, or q4m if you have ~5-6GB VRAM Free.
6. Run the main script `python .\main.py` once, to generate the ".\config.ini" file, then close mantella, and configure the ".\config.ini" after its created. Ensure to also implement updates from `.\config_ini_updates.txt` to ".\config.ini".
7. Run Fallout 4/Skyrim, and then run the `Mantella-WT.Bat` batch, it will, as required, clean the ".\config.ini" and backup the old version to ".\config.bak", and then run "Mantella-WT".

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



- Dynamic switching between, prompt sets and for differing context, depending upon the maximum context for the model, we could switch between ONLY 4096, 8192, in the mantella scripts, depending upon the value of "custom_token_count", I want 2 versions of the characters.csv details, one should have 1 sentence description, the other 2, so as to use the better one for the higher context. 

- Need to remove warning, and streamline code for context assessment, and use the setting from the config.ini, then user can toggle the context lengths from the menu.

# Disclaimer
- This is a fork by Wiseman-Timelord, meaning, if you have issues with the program, its Likely not my code, you would have to check that.
- My forks sometimes just up and dissapear, this tends to happen when I no longer use the relating program, to neaten up things a little.
