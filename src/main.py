import json

import getpass

from modules.seleniumLogic import SeleniumLogic

if __name__ == '__main__':

    with open("./data/data.json") as f:
         data = json.loads(f.read())

    print(data["startup_message"])

    while True:
        print("\n<Login>")
        username, password = input("Username: "), getpass.getpass("Password: ")
        login = SeleniumLogic(username, password)
        rogue_login = login.logic()
        rogue = rogue_login.login()
        if rogue:
            print(f"Logged in as: {username.capitalize()}")
            break
        else:
            print("Incorrect credentials")

    func = {
        "1": rogue.update_all,
        "2": rogue.starter_edit,
        "3": rogue.unlock_all_starters,
        "4": rogue.egg_gacha,
        "5": rogue.edit_pokemon_party,
        "6": rogue.unlock_all_achievements,
        "7": rogue.unlock_all_gamemodes,
        "8": rogue.unlock_all_vouchers,
        "9": rogue.pokedex,
        "10": rogue.biomes,
        "11": rogue.moves,
        "12": rogue.add_candies,
    }

    term = [
        "**************************** ONLINE EDITOR ****************************",
        "1: Update all Data on the Server (Working)",
        "2: Edit a starter (Working)",
        "3: Unlock all starters (Working)",
        "4: Edit your egg-tickets (Working)",
        "5: Edit CURRENT Pokemon Party (Working)",
        "6: Unlock all achievements (Working)",
        "7: Unlock all gamemodes (Working)",
        "8: Unlock all vouchers (Working)",
        "9: Show all Pokemon ID (Working)",
        "10: Show all Biome IDs (Working)",
        "11: Show all Move IDs (Working)",
        "12: Add candies to a pokemon",
        "--------------------------------------------------------------------"
    ]

    while True:
        print("\n".join(term))
        command = input("Command: ")

        if command in func:
            func[command]()
        elif command == "exit":
            quit()
        else:
            print("Command not found")