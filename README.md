# Mantella-WT - Wiseman-Timelords Mantella Optimization
This is a fork, [main is here](https://github.com/art-from-the-machine/Mantella)

# Development 
- The general idea is to improve the speed of conversation, initialization and interaction. Its my opinion that a ok and fast, answer from AI is better than waiting for a quality response, especially in fps, and in relevance to Fallout 4/Skyrim, these are meant to be 100% offline, so I am leaning towards local models heavily. this may involve...
1. Dynamic switching between, prompt sets and for differing context, depending upon the maximum context for the model, we could work up to that, possibly we could switch between 2000, 4000, 8000, however, we would also not just use the maximum all the time. 
2. Potentially 3 versions of the characters .csv, 1/2/3 sentence description limit for each character.
3. Context could also be dynamic, in that we would use the 2k context for greeting, 4k for the continuation with recent history summary or something, 8k for the rest of the convo with full convo history?? A flag will be reset when convo ends, thus enabling quick interactions to begin as required.
4. Some of the inputs, can actually be dynamic, and not present at all in user interaction, most/some of this could scale based on context size and be reasonable settings, see examples in "other notes" section.

# Description
- The edits to actual mantella code will be intended for v11, until they get v12 relesaed, but may also be compatible with v12. Currently there is something wrong with the communication between the, fallout 4 mod and mantella, in v12, so I cant test it for that, nor skyrim (though I am programming it for both as I go). So these updates are to be considered for speeding up Mantella in Fallout 4.

# Features
Work done currently includes...
1. Batch launcher, that launches BOTH, xVASynth in non-Admin AND Mantella in Admin, the batch saves time and messing around.
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
xVASynth.exe is not running.
Running VASynth and Mantella...
Mantella currently running for Fallout4 (D:\GamesVR\Fallout4_163). Mantella mod located in D:\GamesVR\Fallout4_163\Data
09:48:38.551 INFO: Running Mantella with local language model
09:48:38.552 WARNING: Local language model has a low token count of 4096. For better NPC memories, try changing to a model with a higher token count

Mantella v0.11.4
09:48:38.801 TTS: Connecting to xVASynth...

"NPC not added. Please try again after your next response"? See here:
https://art-from-the-machine.github.io/Mantella/pages/issues_qna

Waiting for player to select an NPC...


```

# Usage / Install
1. Ensure the Mantella mod is installed for Fallout/Skyrim from the Nexus mods site.
2. Install [Mantella 11.4](https://github.com/art-from-the-machine/Mantella/releases/tag/v0.11.4).
3. Download the [Mantella-WT Zip File](https://github.com/wiseman-timelord/Mantella-WT/archive/refs/heads/main.zip), drop the files into the main Mantella folder, preserving folders.
4. Install/move xVASynth to `.\ExampleMantellaDirectory\xVASynth`, keeping things tidy. If you did move xVASynth, then click "Reset Paths" in the configuration. 
5. Ensure you have LM Studio or whatever with a kickass model. I currently advise [this one from huggingface.co](https://huggingface.co/Lewdiculous/L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix). I also advise a, q3/q4 (lower is faster) and gguf, version of a model, and run it on 4096 context (this is the default for unrecognised models), even if it has a =>8k context, because speed. 
6. Run the `Mantella-WT.Bat` batch once, to generate the "config.ini" file, then close mantella, and...
6a. For v11, configure the ".\config.ini" after its created. Ensure to implement updates from `.\config_ini_updates.txt` to ".\config.ini".
6b. for v12, the configurator will load in a browser next time you run the program, you will need to set that up there, then close mantella.
7. Run Fallout 4/Skyrim, and then run the `Mantella-WT.Bat` batch.

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
- This is the more concise code for the ini from Nexus.
```
skyrim_multi_npc_prompt = Not needed.

fallout4_prompt = You are {name} in the post-apocalyptic Commonwealth of Fallout. This is your background: {bio}. In-game events will be shown between ** symbols for context. You're having a conversation with {trust} (the player) in {location}. The time is {time} {time_group}. This script will be spoken aloud, so keep responses concise. Avoid, numbered lists or text-only formatting or descriptions, instead speech ONLY. If the player is offensive, start with 'Offended:'. If they apologize or to end combat, start with 'Forgiven:'. If convinced to follow, start with 'Follow:'. The The conversation is in {language}. {conversation_summary}

fallout4_multi_npc_prompt = The following conversation in {location} in the post-apocalyptic Commonwealth of Fallout is between {names_w_player}. Their backgrounds: {bios}. Their conversation histories: {conversation_summaries}. The time is {time} {time_group}. This script will be spoken aloud, so keep responses concise. Avoid, numbered lists or text-only formatting or descriptions, instead speech ONLY. Provide NPC responses, starting with the speaker's name, e.g., '{name}: Good evening.' Decide who should speak as needed (sometimes all NPCs). Respond only as {names}. Use full names. The conversation is in {language}.

radiant_start_prompt = Start or continue a conversation topic (skip greetings). Shift topics if current ones lose steam. Steer toward character revelations or drive previous conversations forward.

radiant_end_prompt = Wrap up the current topic naturally. No need for formal goodbyes as no one is leaving.

memory_prompt = Summarize the conversation between {name} (assistant) and the player (user)/others in {game}. Ignore communication mix-ups like mishearings. Summarize in {language}, capturing the essence of in-game events.

resummarize_prompt = Summarize the conversation history between {name} (assistant) and the player (user)/others in {game}. Each paragraph is a separate conversation. Condense into a single paragraph in {language}.
```
- Some new code to enhance local model ease of use.
```
Drop in your preferred Llama.Cpp Pre-Compiled binaries? All I can think of for now. 
```


# Disclaimer
- This is a fork by Wiseman-Timelord, meaning, if you have issues with the program, its Likely not my code, you would have to check that.
- My forks sometimes just up and dissapear, this tends to happen when I no longer use the relating program, to neaten up things a little.
