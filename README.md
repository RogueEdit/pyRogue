# pyRogue
> **pyRogue** is a educational project. This is mostly to be done, if you have any ideas or problems please use the issue feature.

[<img src="https://img.shields.io/badge/Windows-blue">](https://github.com/RogueEdit/onlineRogueEditor/releases/download/v0.1.7.0/pyRogue-Windows.zip) [<img src="https://img.shields.io/badge/Virus%20Total-blue">](https://www.virustotal.com/gui/file/276dec1526d5c49d1a21930384d19105c8f0221ad4f44754e1a640b7ed25f957?nocache=1) <img src="https://img.shields.io/badge/Checksum-276dec1526d5c49d1a21930384d19105c8f0221ad4f44754e1a640b7ed25f957-blue"> 

[<img src="https://img.shields.io/badge/Linux-Green">](https://github.com/RogueEdit/onlineRogueEditor/releases/download/v0.1.7.0/pyRogue-Linux.zip) [<img src="https://img.shields.io/badge/Virus%20Total-Green">](https://www.virustotal.com/gui/file/6e51af9985ea755e824236fe58fcc3bc938bb233babb5bee7f23731b836d8916?nocache=1) <img src="https://img.shields.io/badge/Checksum-6e51af9985ea755e824236fe58fcc3bc938bb233babb5bee7f23731b836d8916-Green"> 

[<img src="https://img.shields.io/badge/Mac-silver">](https://github.com/RogueEdit/onlineRogueEditor/releases/download/v0.1.7.0/pyRogue-MacIntel.zip) [<img src="https://img.shields.io/badge/Virus%20Total-silver">](https://www.virustotal.com/gui/file/e6fea4986ccaf726df66516561b9bf3180d45118a7ec7a8d6b6c820d78d72add?nocache=1) <img src="https://img.shields.io/badge/Checksum-e6fea4986ccaf726df66516561b9bf3180d45118a7ec7a8d6b6c820d78d72add-silver"> 


![Preview Image](.github/previews/main.png)
![Preview Image](.github/previews/tool.png)

[More examples](PREVIEW.md)
[<img src="https://img.shields.io/badge/Join%20our%20News-Discord!-8A2BE2">](https://discord.gg/AjYYudvX)

# List of content
- [Foreword](https://github.com/RogueEdit/onlineRogueEditor?tab=readme-ov-file#important-foreword)
- [FAQ](https://github.com/RogueEdit/onlineRogueEditor?tab=readme-ov-file#faq)
- [How to use](https://github.com/RogueEdit/onlineRogueEditor?tab=readme-ov-file#how-to-use-the-tool)
- [License](https://github.com/RogueEdit/onlineRogueEditor?tab=readme-ov-file#license)
- [Features](https://github.com/RogueEdit/onlineRogueEditor?tab=readme-ov-file#editor-features)
- [How to run from code](https://github.com/RogueEdit/onlineRogueEditor?tab=readme-ov-file#how-to-run-from-code)
- [Regarding Bans and Limited Accounts](https://github.com/RogueEdit/onlineRogueEditor?tab=readme-ov-file#regarding-bans-and-limited-accounts)

## Important foreword
[Feature & Bugboard aswell as Roadmap](https://github.com/orgs/RogueEdit/projects/7)

We will not sent you any files or contact you about anything. You can see who contributed and everything regarding us will be only done on GitHub. We will not contact you in any matter or will send you files. There are scammers out there. Here you can read the full source code, compile it from scratch and such or download a VT-checked official release.

The AntiVirus might label it as a virus. All the source code is available into the `src/` folder, everything is open readable. This is to be expected on some environments due the nature of such tools. AV's do not like doing static calls via consoles. But you can read every action and exception here in the code.

Attention: When ever this tool detects you are trying to manipulate a daily seeded run it will abort.

If there is any error or cancel of action IT WILL DO tell you!!

If you are intending to use this Tool on a new account you have to atleast kill one pokemon and progress to stage 2. This ensures you will have some savedata that also can be manipulated.

When you launch the tool and login it will create a trainer.json - this is your save-data and is very precious. Please make a copy of it just in case anything goes wrong. - We take no responsibility for your actions when using this script. 

We will not use the tool 24/7 - this means we will not see when it breaks due to changes on PokeRoGue's site. Please report on our discord or GitHub whenever you cannot finish any action.

**IMPORTANT**
When you encounter multiple 403 Forbiddens - it's usually not on us. Retry to a later point or contact us to rebuild a new header seed file. We programmed a hotfix method in for this case.


## FAQ

- How do i revert my changes?
  - The programm will always create backups everytime you login! When you load the first time it will create a `base_[trinerID].json` unique based on your trainerID. All subsequent backups will be named `backup_YearMonthDay_HourMinuteSeconds.json` and you can restore to any file back in time.

  ![Preview Image](.github/previews/backup.png)

- Will this get me banned?
  - See [Regarding Bans and Limited Accounts](https://github.com/RogueEdit/onlineRogueEditor?tab=readme-ov-file#regarding-bans-and-limited-accounts)

- Where can i donate?
  - We will not accept any money or any form of payment. If you want to help then only by contributing.

- Why are some features limited?
  - In our core we don't like cheating. This is and will be mostly for educational purposes, if you want to edit your money and such in daily runs theres other options. We deny any changes made to gameMode 3 which is daily seeded runs.

## How to use the tool

- Step 1: Download the release according to your operating system
- Step 2: Extract the archived data you downloaded
- Step 3: Navigate into the compiled/ folder and launch `pyRogue-[yourOperatingSystem]`
- Step 4: Enter your login data. Your password is in a hidden field. You are entering despite it doesnt look like it. Just login!
- Step 5: Use any actions directed by the tool
- Step 5.5: You also can edit all your jsons manually and afterwards update to server
- Step 6: Update all to server (yellow marked entry: Use when Done)

## License

- If you want to use the code in any manner feel free to do so but make sure you can see immediately its not the official Repo. If you wanna fork it we ask you to change the title in the readme.md -  but if you want to use it anywhere public, lets say replit and such or you wanna add onto this code you have to include all author-headers and in accordance with GPL you also need to keep the license and cannot change it but are free to do everything aslong as you keep the statement before true and our headers. We also prohibit you to make any money of it and we also never will. TLDR; Keep the notice and do what you want even with advanced code but make sure it doesnt look like our program.
 
## Editor Features

- Autocomplete recomendations

![Preview Image](.github/previews/autocomplete.png)

- When encountering multiple 403's can rebuild headers from remote source *NEW*
- Extensive logging for easy debug
- Two login logics to provide some fallbacks

- When logging in it will automatically create backups for you.
  - You can restore backups easily see preview above


- Load data from server
  - This will fetch the trainer.json containing your account save data

- Load Save-slot data from server
  - This will fetch slot_{digit}.json containing data about a current run

- Edit a starter - This will ask you to take multiple inputs:
  - Unlock all hidden forms? (Dressed Peekachu etc.)
  - Should it be shiny? (T1, T2, T3)
  - How many times have you hatched it?
  - How many times have you caught it?
  - How many times have you seen it?
  - How many friendship-candys should it have?
  - All 6 IV's
  - Should it have its passive unlocked? 
  - Should the cost be reduced?
  - Should it have all abilites?
  - Should it have a specific nature or all?

- Unlock all starters | same as above but for all pokemons
  - This will unlock every single Pokemon depending on your choosings like above

- Modify the number of egg-tickets you have
  - This allows you to set the amount of egg gacha tickets you have of every tier
  - due to changes on PokeRoGue's Site this is now limited to certain amounts.
  - This was reverted; https://github.com/pagefaultgames/rogueserver/commit/0526c7a0f197ecec009cbd59b9e07cab00b01a44 but we still keep it limited.

- Edit a pokemon in your party
  - Let's you edit moves, species and level of a Pokemon in your team. It let's you set it shiny and its variant and makes it 6 IVs

- Unlock all achievements
- Unlock all game modes
  - Unlocks: classic, endless, spliced endless
- Add one or unlock all vouchers

- Edit candies on a pokemon
- Edit amount of money
- Edit pokeballs amount
- Edit biome
- Generate eggs
  - Depending on your liking, whatever rarity - gacha type and such
- Set your eggs to hatch
- Edit account stats
- Unlock everything
  - Just calls mulitiple features from above
  - Will also edit account stats with "legit" constraints. Based on your seen variables and such and randomized between reasonable values.

- Create a backup
- Restore a backup

- Display all Pokemon with their names and id
- Display all Biomes IDs
- Display all Moves IDs
- Display all Voucher IDs
- Display all Natures
- Display all Nature Slot IDs
- Save data to server via open accesible API calls

- Propper logging in case you need to troubleshoot

## How to run from code
 - Install python
 - Download the source code
 - Extract the source code
 - Open a terminal, navigate into your `[extracted_folder]/src/`
 - Install all the requirements using python according to setup
   - `python3 -m pip install -r requirements.txt`
 - Now you should be able to run main.py
   - `python3 main.py`

## Regarding Bans and Limited Accounts
https://www.reddit.com/r/pokerogue/comments/1d8hncf/cheats_and_exploits_post_followup_bannable/
https://www.reddit.com/r/pokerogue/comments/1d8ldlw/a_cheating_and_account_deletionwipe_followup/


<meta name="keywords" content="pokerogue, pokerogue save editor, pokerogue, rogueEditor, free, gacha, ticket, tickets, egg, eggs, shiny, save, edit, pokemon, unlimited, hack, hacks, cheat, cheats, trainer, table, pokedex, dex, wave, money, level, levels, iv, ivs, stat, stats, item, items, api, mod, mods, tool, tools, education, python">