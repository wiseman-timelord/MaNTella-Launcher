# Mantella-WT - Wiseman-Timelords, Mantella Optimization / Launcher.
This is a fork, in the form drop-in files and optimizations to perform, main is [here](https://github.com/art-from-the-machine/Mantella).

# Description
- The edits to actual mantella code will be intended for v11, until they get v12 relesaed, but may also be compatible with v12. Currently there is something wrong with the communication between the, fallout 4 mod and mantella, in v12, so I cant test it for that, nor skyrim (though I am programming it for both as I go). So these updates are to be considered for speeding up Mantella in Fallout 4.

# Features
Work done currently includes...
1. Batch launcher, that launches BOTH, xVASynth in non-Admin AND Mantella in Admin, the batch saves time and messing around, if you install xVASynth to the suggested folder, it will, as required, automatically run it too.
2. Concise Chararacter details. The Skyrim character details were non-standardized, and generally both had too much info.
3. Concise, optimized and streamlined, prompts for config.ini, with stated charater limit on consolidation. follow, offended, forgiven were removed, as they didnt work in vanilla when tested.

# Preview
- Uh, theres the batch launcher...
```
==============================================================================
                         Mantella / xVASynth Launcher
------------------------------------------------------------------------------

Administrator Mode.
Current Directory: D:\GamesVR\Mantella-0.11.4
Checking for running xVASynth.exe process...
xVASynth.exe is already running. Continuing to Mantella...
Running Mantella...
Mantella currently running for Fallout4 (D:\GamesVR\Fallout4_163). Mantella mod located in D:\GamesVR\Fallout4_163\Data
12:02:10.244 INFO: Running Mantella with local language model
12:02:10.245 WARNING: Local language model has a low token count of 4096. For better NPC memories, try changing to a model with a higher token count

Mantella v0.11.4
12:02:10.464 TTS: Connecting to xVASynth...
12:02:10.623 STT: Audio threshold set to 'auto'. Adjusting microphone for ambient noise...
12:02:10.623 STT: If the mic is not picking up your voice, try setting this audio_threshold value manually in MantellaSoftware/config.ini.


"NPC not added. Please try again after your next response"? See here:
https://art-from-the-machine.github.io/Mantella/pages/issues_qna

Waiting for player to select an NPC...


```

# Usage / Install
1. Ensure the Mantella mod is installed for Fallout/Skyrim from the Nexus mods site.
2. Install [Mantella 11.4](https://github.com/art-from-the-machine/Mantella/releases/tag/v0.11.4) to a suitable directory.
3. Download the [Mantella-WT Zip File](https://github.com/wiseman-timelord/Mantella-WT/archive/refs/heads/main.zip), drop the files into the main Mantella folder, preserving folders.
4. Install/move xVASynth to `.\ExampleMantellaDirectory\xVASynth`, keeping things tidy. If you did move xVASynth, then click "Reset Paths" in the configuration.  If you do not have xVASynth installed to my suggested folder, then remember to run it first.
5. Ensure you have LM Studio or whatever with a kickass model, and if you are AMD user, ensure it is LM Studio v0.2.31, as this supports Vulkan. Currently I advise this model [this one from huggingface.co](https://huggingface.co/Lewdiculous/L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix). I also advise a, lower and faster, version, such as q3 s/m (xxs was not satisfactory), and run it on 4096 context in LM Studio AND Mantella (default will be 4096 for unrecognised, thats what we need for this model).
6. Run the `Mantella-WT.Bat` batch once, to generate the "config.ini" file, then close mantella, and...
6a. For v11, configure the ".\config.ini" after its created. Ensure to implement updates from `.\config_ini_updates.txt` to ".\config.ini".
6b. for v12, the configurator will load in a browser next time you run the program, you will need to set that up there, then close mantella.
7. Run Fallout 4/Skyrim, and then run the `Mantella-WT.Bat` batch.

# Development 
- The general idea is to improve the speed of conversation, initialization and interaction. Its my opinion that a ok and fast, answer from AI is better than waiting for a quality response, focus is on local models/processing. this may involve...
1. Dynamic switching between, prompt sets and for differing context, depending upon the maximum context for the model, we could work up to that, possibly we could switch between 2000, 4000, 8000, themed content, so as for less to process in appropriate situation. Potentially 3 versions of the characters .csv, 1/2/3 sentence description limit for each character. 2k context for greeting, 4k for the continuation with recent history summary or something, 8k for the rest of the convo with full convo history? First time is full context because probably wont use it all and will want best quality response, as speak to most for one or two times. possibly llm could decide based on previous answers to extend or retract, context by requesting addition of preferences for relevant things at end of prompt? Maybe A flag will be reset when convo ends, thus enabling quick interactions to begin as required.
2. Some of the inputs, can actually be dynamic, and not present at all in user interaction, most/some of this could scale based on context size and be reasonable settings, see examples in "other notes" section.
3. Put menu on batch launcher...
```
=================================
Mantella-WT
---------------------------------

1. Run Mantella / xVASYnth
2. Optimization: Faster/Medium/Quality

---------------------------------
Selection, Options 1-2, Exit = X:

```


# Other Notes (developed from original post on nexus)
- Dynamic Context
```
2048
max_tokens = 100
max_response_sentences = 1
temperature = 0.4

4096
max_tokens = 125
max_response_sentences = 2
temperature = 0.5

8192
max_tokens = 150
max_response_sentences = 2
temperature = 0.6
```
... the maximum allowed context would also work together with the auto model selection, because the user would be able to therein set the maximum they intend to use. Maybe they just want to use 2k on a 8k model for speed, but if they want to wait for local processing or they are using gpt4, then they would choose to set higher.
```
Drop in your preferred Llama.Cpp Pre-Compiled binaries? All I can think of for now. 
```


# Disclaimer
- This is a fork by Wiseman-Timelord, meaning, if you have issues with the program, its Likely not my code, you would have to check that.
- My forks sometimes just up and dissapear, this tends to happen when I no longer use the relating program, to neaten up things a little.
