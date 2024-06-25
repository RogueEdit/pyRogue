# pyRogue
> ## **pyRogue** is a **educational** project. 
<img src="https://img.shields.io/badge/Make_sure_to_mark_with_a-Star_<3-Red">

Based on the Source Code of pokerogue.net - https://github.com/pagefaultgames/pokerogue
> In compliance with Pokerogue's License this project here is also released under AGPL3.

![Preview Image](.github/previews/main.png)
![Preview Image](.github/previews/tool.png)

[Regarding Bans and Limited Accounts - actions with this tool can cause you to be limited.](https://github.com/RogueEdit/onlineRogueEditor?tab=readme-ov-file#regarding-bans-and-limited-accounts)

# List of content
- [Important Foreword](https://github.com/RogueEdit/onlineRogueEditor?tab=readme-ov-file#important-foreword)
- [FAQ](https://github.com/RogueEdit/onlineRogueEditor?tab=readme-ov-file#faq)
- [How to use](https://github.com/RogueEdit/onlineRogueEditor?tab=readme-ov-file#how-to-use-the-tool)
- [How to run from code](https://github.com/RogueEdit/onlineRogueEditor?tab=readme-ov-file#how-to-run-from-code)
- [License](https://github.com/RogueEdit/onlineRogueEditor?tab=readme-ov-file#license)
- [Features](https://github.com/RogueEdit/onlineRogueEditor?tab=readme-ov-file#editor-features)
- [Regarding Bans and Limited Accounts](https://github.com/RogueEdit/onlineRogueEditor?tab=readme-ov-file#regarding-bans-and-limited-accounts)

## Important foreword

We learned enough about freezing python to binarys so from here on out it will be source code only.

We will not sent you any files or contact you about anything. You can see who contributed and everything regarding us will be only done on GitHub. We will not contact you in any matter or will send you files. There are scammers out there. Here you can read the full source code, compile it from scratch and such or download a VT-checked official release.

Attention: When ever this tool detects you are trying to manipulate a daily seeded run it will abort. We only do this for educating us.

- We take no responsibility for your actions when using this tool.

## FAQ

- How do i revert my changes?
  - The programm will always create backups everytime you login! When you load the first time it will create a `base_[trinerID].json` unique based on your trainerID. All subsequent backups will be named `backup_YearMonthDay_HourMinuteSeconds.json` and you can restore to any file back in time.

  ![Preview Image](.github/previews/backup.png)

- Will this get me banned?
  - See [Regarding Bans and Limited Accounts](https://github.com/RogueEdit/onlineRogueEditor?tab=readme-ov-file#regarding-bans-and-limited-accounts)

- Where can i donate?
  - We will not accept any money or any form of payment. If you want to help then only by contributing.

## How to use the tool

- **Step 1:** Download the correct compiled up2date version
- **Step 2:** Extract the archived data you downloaded
- **Step 3:** Navigate into the compiled/ folder and launch `pyRogue-[yourOperatingSystem]`
- **Step 3.5:** Log out of pokerouge, do not login or interfere while editing.
- **Step 4:** Enter your login data. Your password is in a hidden field. You are entering despite it doesnt look like it. Just login!
- **Step 5:** Use any actions from the menu
  - **Step 5.5:** You also can edit all your jsons manually and afterwards update to server
- **Step 6:** Update all to server (yellow marked entry: Use when Done)

## How to run from code
- Install python
- Download the source code
- Extract the source code
- Open a terminal, navigate into your `[extracted_folder]/src/`
- Install all the requirements using python according to setup
  - `python3 -m pip install -r requirements.txt`
- Now you should be able to run main.py
  - `python3 main.py`


## License

- See license document and credit headers. 
 
## Editor Features
- Autocomplete recomendations

![Preview Image](.github/previews/autocomplete.png)
- **Extensive logging for easy debug in log file
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

- Item Editor
![Preview Image](.github/previews/itemEditor.png)

## Regarding Bans and Limited Accounts
https://www.reddit.com/r/pokerogue/comments/1d8hncf/cheats_and_exploits_post_followup_bannable/

https://www.reddit.com/r/pokerogue/comments/1d8ldlw/a_cheating_and_account_deletionwipe_followup/

<meta name="keywords" content="pokerogue, pokerogue save editor, pokerogue, rogueEditor, free, gacha, ticket, tickets, egg, eggs, shiny, save, edit, pokemon, unlimited, hack, hacks, cheat, cheats, trainer, table, pokedex, dex, wave, money, level, levels, iv, ivs, stat, stats, item, items, api, mod, mods, tool, tools, education, python">
