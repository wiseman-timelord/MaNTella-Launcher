# Mantella-WT - Drop-in files for Optimization and Enhancement of original scripts. 
Status: Project being re-planned.  Notice: Some of the details are somewhat inaccurate, at-least until the next release.

# Description
So far character descriptions have basic details and 1 sentence description, this helps greatly with faster processing, however, they need to be re-done, to have 2-3 sentences per character. Soon there willbe 2 batches. The batch/python standalone launcher has moved to [Mantella-Local-Launcher](https://github.com/wiseman-timelord/Mantella-Local-Launcher).

# Features
This section is being re-done, however...
- There will be a "Setup-Install.Bat", for requirements, to make things fool-proof.
- There will be a "Run_Mantella.Bat", this will have the epic batch code from the Launcher.
- There will be enhanced versions of main branch scripts, that will be pushed to main or not, 

# Preview
- The working of the thing, is pretty much the same as Mantella currently, there will be an update here when there is something to show.

## Requirements
1. **Python Environment**: Requires Python 3.11 and dependencies from the Mantella requirements file.
2. **Language Model**: Use [Lewdiculous L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix](https://huggingface.co/Lewdiculous/L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix) with Q3 or Q4 VRAM specifications.
3. **Operating System**: Compatible with Windows 7 through Windows 11; administrative privileges will be needed.

# Usage / Install
1. Ensure the [Mantella Mod](https://www.nexusmods.com/fallout4/mods/79747) is installed for Fallout/Skyrim from the Nexus mods site, follow the guide, this will, at some point, require install [Mantella 11.4](https://github.com/art-from-the-machine/Mantella/releases/tag/v0.11.4) to a suitable directory.
2. After completing Mantella 11.4 install, then download the [Latest working Mantella-WT release](https://github.com/wiseman-timelord/Mantella-WT/releases/), drop the files into the main Mantella folder, preserving folders.
5. Configure the ".\config.ini", ensure you have entered things like, "fallout4_folder" and "fallout4_mod_folder" and "llm_api" and "tts_service".
6. Run Fallout 4/Skyrim, and then run the `Run_Mantella.Bat` batch.
- Hopefully you have, Admin rights and sensible system settings, but click allow on firewall as required, I am guessing its the interaction between Mantella and the Mantella Mod.

# Development
- The idea is now to, 1. optimize the scripts, 2. enhance the prompting, therefore, code in mantella-wt will be able to be pushed to main.
- Streamline the scripts for local should become a diff fork Mantella-Local,  Mantella-Local will then become a thing, for people whom will not be using online services. code will be streamlined, streamlining will open up possibilities. Mantella-Local will not be happening until other projects are complete.
- When v12 comes, We will see what happens. 
- requires re-assessment of what is a "Required number of Tokens" for llama 3 level, as noticed it was generating at 1 token per word. 

# Disclaimer
- The extension `-WT` means that this project does not originate from Wiseman-Timelord, it is the "Wiseman-Timelord's" own, "Hack" or "Version", of the relating "Official" software. Any issues regarding the "Original" code, stop with the Author's of the "Original" code.
