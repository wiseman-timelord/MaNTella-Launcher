# Mantella-Local-Launcher for [Mantella](https://github.com/art-from-the-machine/Mantella/releases)
Status: Under Development, Today release, and mods back on nexus, one is hoping....
- Patching up some unforseen differences between v11.4 and v12. 
- Re-Structuring of script, sorting out sections into themes of code is important for large scripts. 
- Optimization through intellgent code and merging functions, possibly involving additional global for function program pre-configuration.
- Logic and sanity checks, general checkovers of code.

### Description
- a Windows Installer/Optimizer/Launcher for Mantella for, Fallout 4/Vr and Skyrim Se/Ae/Vr, specifically only for local models on Windows through, Ollama or LM Studio. Mantella was optimized for 8K on GPT, so, Mantella-Launcher instead optimizes Mantella for Local Models. The script facilitates pre-launch, configuration management and optimization, launches, xVASynth and your chosen game, if they are not already running, then it launches Mantella, by making use of the settings already present in `config.ini`, so you do still need to configure that first. Mantella-Launcher also performs various tasks such as, cleaning configuration files and optimizing the mantella prompts. The Batch file manages the, communication between and launching, of the relevant programs/scripts, while the Python component of the script handles the heavy work, and displays an interactive menu for user selection of game and optimization options. 

### Features
- **Batch Launcher for Automation**: Automates and runs xVASynth and Mantella with admin privileges.
- **Optimized Configuration Management**: Streamlines `config.ini` prompts and removes non-functional options.
- **Interactive Python Script**: Cleans configuration files and offers an interactive menu for game and preset choices.
- **Automatic Execution and Exit Handling**: If not already running, then runs, Fallout 4 and/or xVASynth, and then continues to Mantella for smooth operation.
- **LM Studio / Ollama Support **: Switch models to similar one with different name, and it is handled by the launcher in `config.ini`.
- **Auto-Optimize Prompts**: Prompts are upgraded/streamlined, character sheets will be optimized based on context, but that part is still being worked on.
- **Auto-Environment Selection**: Code enables python location to be found, and correct version of python to be used. 
- **Persistent Settings**: The scripts create/uses, `.\data\persistence.txt` and `config.ini`, your settings are saved.

### Preview
- The `Pre-Launch Configuration` options of `Mantella-Launcher.Bat`...
```
========================================================================================================================
    Pre-Launcher Configuration
========================================================================================================================









    1. Mantella-Local-Launcher

    2. Just Run Mantella

    3. Installer-Setup









========================================================================================================================
Selection; Menu Options = 1-3, Exit Batch = X:

```
- The `Mantella-Local-Launcher` provides simplified, configuration and optimization...
```
=======================================================================================================================
    MaNTella-Local-Launcher
-----------------------------------------------------------------------------------------------------------------------

    1. Select Game Used
        (Fallout4VR)
    2. Prompt Optimization
        (Regular)
    3. Model Token Count
        (4096)
    4. Voice Input Cutoff
        (2s)
    5. Launch WebUI Config
        (False)

-----------------------------------------------------------------------------------------------------------------------

    Fallout4VR_Path:
        C:\Games\Steam\steamapps\common\Fallout4VR
    xVAsynth Path:
        C:\Games\Steam\steamapps\common\xVASynth\xVASynth.exe
    LLM API:
        OpenRouter
    Model Loaded:
        uncensored-frank-llama-3-8b.q6_k

=======================================================================================================================
Selection, Program Options = 1-5, Refresh Display = R, Begin Mantella/xVASynth/Fallout4 = B, Exit and Save = X:

```
- The `Installer-Setup`, to install requirements compitently...
```
========================================================================================================================
    Installer-Setup
========================================================================================================================


    1. Install `.\requirements.txt`

    2. First Run Setup (Run Once)

    3. Fix Ollama Non-Cuda/Non-Rocm GPU

    4. Upgrade Pip Version

    5. Check Dependency Conflicts

    6. File Integrity Test

------------------------------------------------------------------------------------------------------------------------

    Python Path:
        C:\Users\Mastar\AppData\Local\Programs\Python\Python311\python.exe

    Config File:
        F:\Documents\My Games\Mantella\config.ini


========================================================================================================================
Selection; Menu Options = 1-6, Back to Main = B:

```

## Requirements
1. **Powerful Computer**: Running Fallout 4/Skyrim and interference on models can be intensive.
4. **Operating System**: Compatible with Windows 7 through Windows 11; administrative privileges may be needed.
2. **Python Environment**: "Mantella-Local-Launcher requires Python 3.11", but Ensure that it was installed to the default directory or the default directory for all users.
3. **Python Libraries**: The same libraries as Mantella listed in `requirements.txt`.
3. **LM Studio or Ollama**: Obtain model folder/name and foolproofs api config, Mantella-Local-Launcer will not work on non-local model host services.
4. **Language Model**: Search [HuggingFace](https://huggingface.co) for a `.Gguf` model such as, llama 3 or llama 3.1, 4.xGB VRam Free for Q3 or 5.xGB VRam free for Q4, and for shared GPU this is in addition to whatever Fallout 4 consumes of your Vram.
5. **Mantella Installation**: It was made for the v12 version on [Github](https://github.com/art-from-the-machine/Mantella/releases), other versions will work likely unless they change the key names. The files from Nexus are likely always going to be compatible, heres the link for, [Fallout 4](https://www.nexusmods.com/fallout4/mods/79747) and [Skyrim](https://www.nexusmods.com/skyrimspecialedition/mods/98631).
5. **xVASynth Installation**: Must be installed and correctly configured in the specified directory.

# Usage / Install
1. Ensure the, [Fallout 4 Mantella Mod](https://www.nexusmods.com/fallout4/mods/79747) or [Skyrim SE/AE Mantella Mod](https://www.nexusmods.com/skyrimspecialedition/mods/98631), is installed for from the Nexus mods site to relevantly, fallout 4 or skyrim SE/AEm, and ensure to skim through the relating guides, this will require install [Mantella v12](https://github.com/art-from-the-machine/Mantella/releases/tag/v0.12) to a suitable directory.
2. Download the most recent version of [Mantella-Local-Launcher](https://github.com/wiseman-timelord/Mantella-Local-Launcher/releases), and drag the, file(S) and folder(s), from the zip into the main Mantella folder.
3. Run `Mantella-Launcher.Bat`, and ensure to select `3. Installer-Setup`, to assist in the processes of installing requirements compitently, or if you had issues with the instructions in the guide, this may help you with certain parts of the process. Also ensure that you have ran `First Run Setup`, and filled in the `Mantella Webui Configuration` appropriately in the browser that will pop up. 
<br>3a. For Ollama, if, you are getting Torch errors and/or you do not have suitable GPU, then install `Torch[Cpu]`, to ensure Ollama uses CPU libraries instead. 
<br>3b. For LM Studio, to Quote "In config.ini, set llm_api = http://localhost:1234/v1/. This is the URL that LM Studio is running your model on.".
<br>3c. For Other methods of hosting models, they are detailed in the Official guides, I cannot confirm they will work, they probably wont. 
5. Go back to the main menu in `Mantella-Launcher.Bat`, select `1. Mantella-Local-Launcher` for the Game Launcher, therein, configure your preferences from options 1-4, and when done then select "B" for begin. 
- If for some reasoning there are issues with mantella or mantella crashes, then you can at any point, close the mantella window, and run `Mantella-Launcher.Bat`, and instead select `2. Just Run Mantella`, to re-start mantella, which I found works to fix issues of mantella having issues where the User is somehow locked into a conversation, and unable to start new conversations.
  
## Notes
- all options for Optimization are shown...
```
Default: max_tokens = 250, max_response_sentences = 999, temperature = 1
Faster: max_tokens = 100, max_response_sentences = 1, temperature = 0.4
Regular: max_tokens = 150, max_response_sentences = 2, temperature = 0.5
Quality: max_tokens = 200, max_response_sentences = 3, temperature = 0.6
```
- The System Prompt, on your Model Server (LM Studio) or that you used to install the model (Ollama), should be something like "You are, to requirement, an AI, role-player and text processor, you will be instructed to either be, roleplaying with the Player/NPCs."...
<img src="./media/lm_studio_prompt_mantella.jpg" align="center" alt="no image" width="313" height="315">.
- If you are using one graphics card for, game and model, then ensure to use nVidia/Amd control panels to monitor free ram when fallout 4 is running, the amount of free space with small additional amount for runnings, determines what size of model you will be using.
- a Llama 3 Q3_m model with fallout 4 dlc & ~300 mods including PhyOp performance texture pack, utilizes all of the 8GB on a single card, if you want to use =>Q4 and/or hd textures, then 12GB GPU is suggested, or maybe you have heard of things like PhyOp AI Enhanced Textures.
- There is also my mod collection specifically designed for Mantella, [MWO2 - Mantella Wasteland Operator](https://www.youtube.com/watch?v=ayZmcOqZ8iY), in that, initially the mods from MWO1 that had issues with Mantella were removed.
- If you are looking for the v11.4 files, there is a specific, setup-install and run-mantella, batches, that are separate to the launcher, the latest versions of those are the files I intended for Mantella team to incorporate into Mantella Mod, as I could not push batches to main...which explains why so many programs on github dont have simple batches to take care of basic issues for windows users.  

# Development
1. Need to update the prompts to incorporate the new chat options brought in by v12.
1. All features need double checking. 
2. Clean up redundancy and optimize, and re-test (scripts are large).
3. Now have skyrim again, and will be able to test/auto-optimize the character sheets based on context for, skyrim and fallout.
4. Update relevant media. Character sheet must be backed up  "gamename_characters.bak", and then backup must be used to dynamically in relevance to the context size chosen, be filtered to contain, 2048 = 1 sentences, 4096 = 2 sentences, 8192 = 4 sentences, context lengths should be either, 2048, 4096, 8192, process the gamename_characters.csv according to the current context settings for context, and over-write any existing csv file. It would schedule the character details to be processed, upon the user selecting, `B` or `X`. 
- There is also work on Llama-Legacy-Serve, this will be able hopefully to merge with Mantella-Local-Launcher, `https://github.com/wiseman-timelord/Llama-Legacy-Serve`.
- Idea: could also open in a new window, and then the window for the launcher could be data visualization through libraries designed for that, relating to ollama/lm studio interference? (or would this be too many windows?


## Disclaimer
This software is subject to the terms in License.Txt, covering usage, distribution, and modifications. For full details on your rights and obligations, refer to License.Txt.
