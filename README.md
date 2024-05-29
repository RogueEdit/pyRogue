# OnlineRogueEditor
> **OnlineRogueEditor** is a solution for editing official saves on pokerogue.net!

> [If you are looking for an Editor to edit your Offline-Saves - Check this out](https://github.com/rogueEdit/OfflineRogueEditor)

[<img src="https://img.shields.io/badge/Join%20our%20Discord!-8A2BE2">](https://discord.gg/8ZAnsZfVQP)

![Preview Image](.github/preview.png)

## Important foreword
This tool relies on accurate timings to retrieve and manipulate data. The application will seemingly "sleep" but it will do its thing's. To ensure compatibility of all users across all different connection speeds this is neccesary. 

If there is any error or cancel of action IT WILL DO tell you!!

If you are intending to use this Tool on a new account you have to atleast kill one pokemon and progress to stage 2. This ensures you will have some savedata that also can be manipulated.

When you launch the tool and login it will create a trainer.json - this is your save-data and is very precious. Please make a copy of it just in case anything goes wrong. We take no responsibility for your actions when using this script. 
```

We will not use the tool 24/7 - this means we will not see when it breaks due to changes on PokeRoGue's site. Please report on our discord or GitHub whenever you cannot finish any action.

## How to use the tool

- Step 1: Download the release according to your operating system
- Step 2: Extract the archived data you downloaded
- Step 3: Navigate into the compiled/ folder and launch `onlineEditor-[yourOperatingSystem]`
- Step 4: Enter your login data. Your password is in a hidden field. You are entering despite it doesnt look like it. Just login!
- Step 5: A chrome testsuite will open and process your login and retrieve the needed data. Do not touch anything even after logging in. The Browser will close at some point and process your login in the console.

  - It will look like its doing nothing but this is to ensure accurate results accross any network connection speed. If it will fail it will tell you so!
- Step 6: Now we are logged in and you can type the number of Action you want and follow the instructions.

  - Please do not open a new session of PokeRoGue once you are logged in by the console. This will revert the session and you will need to restart the tool and log in again.
- Step 7: Type the command "1" which is Update all data on the server when you are happy with your edit to load up the data.

- Step 8: Refresh the Page. When everything worked your changes should be applied.

## If you wish to contribute

If you wish to contribute we are always looking for keen people to support the cause. Join our discord or if you want to contribute code you also can simply fork this Repo and start committing!
 
## Editor Features
> - [X] means is working as intended, 
> - [ ] means something is broken :(

- [X] Update all data on the server
- This will sent the local .json file to the server and apply the changes

- [X] Edit a starter
- This will ask you for a pokemonID or a name and will allow you to edit following attributes:
  - Is it shiny?
  - How many times have you seen it?
  - How many times have you caught it?
  - How many times have you hatched it?
  - How many friendship-candys do you want?
  - All 6 IV's

- [X] Unlock all starters
- This will unlock every single Pokemon in the Pokedex with Perfect IVs, All natures, abilities, genders and optional shiny tiers.

- [X] Modify the number of egg gacha tickets you have
- This allows you to set the amount of egg gacha tickets you have of every tier
  - due to changes on PokeRoGue's Site this is now limited to certain amounts.

- [X] Edit a pokemon in your party
- Let's you edit moves, species and level of a Pokemon in your team. It let's you set it shiny and its variant and makes it 6 IVs

- [X] Unlock all achievements
- Unlocks every achievement

- [X] Unlock all game modes
- Unlocks: classic, endless, spliced endless

- [X] Unlock all vouchers
- Currently 5 are somehow not working but apart from that every other 99+ vouchers will be unlocked

- [X] Display all Pokémon with their names and id
- [X] Show all biomes IDs
- [X] Show all moves IDs
- [X] Add friendship-candies to a pokemon

## Deprecated

- [ ] Hatch all eggs
- This will make all your eggs hatch after you defeat 1 Pokemon.
- This was prevented by code changes on PokeRoGue's site.
## Warning

The AntiVirus might label it as a virus. All the source code is available into the `src/` folder, and you can even decompile the exe files; they've been compiled with pyinstaller.

<!-- Metadata: keywords -->
<meta name="description" content="is a solution for editing save files in the offline version for pokerogue written in Python.">
<meta name="keywords" content="pokerogue, pokerogue save editor, pokerogue hacks, pokerogue hack, pokerogue cheats, pokerogue cheat, pokerogue trainer, pokerogue cheat table, rogueEditor, free, gacha, ticket, tickets, egg, eggs, shiny, save, edit, pokemon, unlimited, hack, hacks, cheat, cheats, trainer, table, pokedex, dex, wave, money, level, levels, iv, ivs, stat, stats, item, items, api, mod, mods, tool, tools">
