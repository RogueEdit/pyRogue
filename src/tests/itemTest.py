import json
from colorama import Fore, Style, init
import re

init()

def strip_color_codes(text):
    ansi_escape = re.compile(r'\x1b\[.*?m')
    return ansi_escape.sub('', text)

def line_fill(line, helper_text='', length=55, fill_char=' ', truncate=False):
    stripped_line = strip_color_codes(line)
    stripped_helper_text = strip_color_codes(helper_text)
    total_length = len(stripped_line) + len(stripped_helper_text)
    if truncate and total_length > length:
        truncated_length = length - len(stripped_helper_text) - 3
        line = line[:truncated_length] + '...'
        stripped_line = strip_color_codes(line)
        total_length = len(stripped_line) + len(stripped_helper_text)
    fill_length = length - total_length
    fill = fill_char * fill_length
    return f"{Style.RESET_ALL}{line}{fill}{helper_text}"

def center_text(text, length=55, fill_char=' '):
    stripped_text = strip_color_codes(text)
    total_length = len(stripped_text)
    if total_length >= length:
        return text[:length]
    fill_length = length - total_length
    front_fill = fill_char * (fill_length // 2)
    back_fill = fill_char * (fill_length - (fill_length // 2))
    if fill_char == '>':
        back_fill = '<' * (fill_length - (fill_length // 2))
    return f"{front_fill}{text}{back_fill}"

def initialize_menu(term):
    valid_choices = []
    actual_idx = 1
    for item in term:
        if isinstance(item, tuple):
            if item[1] == 'helper':
                print(Fore.GREEN + '* ' + center_text(f' {item[0]} ', 55, '-') + f' {Fore.GREEN}*' + Style.RESET_ALL)
            elif item[1] == 'title':
                print(Fore.GREEN + '* ' + center_text(f' {item[0]} ', 55, '*') + f' {Fore.GREEN}*' + Style.RESET_ALL)
            elif item[1] == 'category':
                print(Fore.LIGHTYELLOW_EX + '* ' + center_text(f' {item[0]} ', 55, '>') + f' {Fore.GREEN}*' + Style.RESET_ALL)
            else:
                text, func = item
                line = f'{actual_idx}: {text[0]}'
                formatted_line = line_fill(line, text[1], 55, ' ', True)
                print(Fore.GREEN + '* ' + formatted_line + f' {Fore.GREEN}*' + Style.RESET_ALL)
                valid_choices.append((actual_idx, func))
                actual_idx += 1
        else:
            print(Fore.YELLOW + '* ' + center_text(item, 55, '*') + ' *' + Style.RESET_ALL)
    return valid_choices

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def ensure_modifiers_block(data, type_id):
    """Ensure the 'modifiers' block is present and return stack count for given type_id."""
    if 'modifiers' not in data or not isinstance(data['modifiers'], list):
        data['modifiers'] = []

    # Look for existing modifier with matching type_id
    for modifier in data['modifiers']:
        if modifier.get('typeId') == type_id:
            return modifier.get('stackCount', 0)
    return None

def add_or_update_modifier(data, modifier, modifier_name, slot):
    existing = next((m for m in data['modifiers'] if m['typeId'] == modifier['typeId']), None)
    
    if existing:
        existing['stackCount'] = modifier['stackCount']
    else:
        data['modifiers'].append(modifier)
    
    save_json(data, f'slot_{slot}.json')
    print(f'Successfully added {modifier['stackCount']}{modifier_name}')

def user_menu():
    menu_items = [
        ("pyRogue Item Editor", 'title'),
        (("Hidden Ability Rate Booster Modifier", 'Ability Charm'), ABILITY_CHARM),
        (("Shiny Rate Booster Modifier", 'Shiny Charm'), SHINY_CHARM),
        (("EXP Charm", 'EXP Charm'), EXP_CHARM),
        (("Super EXP Charm", 'Super EXP Charm'), SUPER_EXP_CHARM),
        (("Golden EXP Charm", 'Gold EXP Charm'), GOLDEN_EXP_CHARM),
        (("Healing Booster Modifier", 'Healing Charm'), HEALING_CHARM),
        (("On-hit item stealer", 'Mini Black Hole'), MINI_BLACK_HOLE),
        (("Multi-Hit Modifier", 'Multi Lens'), MULTI_LENS),
        (("On-death revive", 'Reviver Seed'), REVIVER_SEED),
        (("Lock Capsule", 'Lock Capsule'), LOCK_CAPSULE),
        (("On-hit item stealer", 'Grip Claw'), GRIP_CLAW),
        (("On-hit money rewarded", 'Golden Punch'), GOLDEN_PUNCH),
        (("EXP Balancer", 'EXP Balance'), EXP_BALANCE),
        (("Rare Candy Booster", 'Candy Jar'), CANDY_JAR),
        (("More money from trainers", 'Amulet Coin'), AMULET_COIN),
        (("Chance to not loose berrys", 'Berry Pouch'), BERRY_POUCH),
        (("Heal-on-hit", 'Shell Bell'), SHELL_BELL),
        (("Pokemon Nature Weight Modifier", 'Soul Dew'), SOUL_DEW),
        (('Give all listed', 'Give all :)'), do_all_modifiers),
        (("Print Modifiers", ''), print_modifiers),
        (("Return to Menu", ''), print_modifiers),
        ("pyRogue Item Editor", 'title'),
    ]

    try:
        while True:
            print('')
            slot = int(input('Select the session slot you want to edit (1-6): '))
            if slot < 1 or slot > 6:
                print('Invalid session slot.')
                continue
            existing_data = load_json(f'slot_{slot}.json')
            valid_choices = initialize_menu(menu_items)
            user_input = input("Command: ").strip().lower()
            if user_input == 'exit':
                raise KeyboardInterrupt  # Raise KeyboardInterrupt to exit the program
            
            # Handle user input
            if user_input.isdigit():
                choice_index = int(user_input)
                for idx, func in valid_choices:
                    if idx == choice_index:
                        function_name = func.__name__
                        if function_name == 'print_modifiers':
                            print_modifiers(existing_data)
                            break

                        slot = int(input('Select the Pokemon slot you want to edit (0-5): '))
                        if slot < 0 or slot > 5:
                            print('Invalid session slot.')
                            continue

                        if function_name == 'do_all_modifiers':
                            stack = int(input('How many all listed modifiers do you want?: '))
                            do_all_modifiers(existing_data, stack, slot)
                            break
                        
                        # Get stack count or prompt for new stack amount
                        stacks_raw = ensure_modifiers_block(existing_data, function_name)
                        if stacks_raw:
                            stack = int(input(f"You already have {stacks_raw} of {function_name}. Set it to: "))
                        else:
                            stack = int(input(f'How many {function_name} do you want?: '))
                        
                        func(existing_data, stack, slot)  # Call the associated function
                        break
                    elif idx == 'exit':
                        raise KeyboardInterrupt()
                else:
                    print("Invalid selection. Please choose a valid menu option.")
            else:
                print("Invalid input. Please enter a number.")

    except KeyboardInterrupt:
        print("Program interrupted by user.")
                                
def ABILITY_CHARM(existing_data, stack, slot):
    modifier = {
        "className": "HiddenAbilityRateBoosterModifier",
        "args": None,
        "player": True,
        "stackCount": 10 if stack > 10 else stack,
        "typeId": "ABILITY_CHARM"
    }
    add_or_update_modifier(existing_data, modifier, "Hidden Ability Rate Booster Modifier", slot)

def SHINY_CHARM(existing_data, stack, slot):
    modifier = {
        "args": None,
        "className": "ShinyRateBoosterModifier",
        "player": True,
        "stackCount": 4 if stack > 4 else stack,
        "typeId": "SHINY_CHARM"
    }
    add_or_update_modifier(existing_data, modifier, "Shiny Rate Booster Modifier", slot)

def EXP_CHARM(existing_data, stack, slot):
    modifier = {
        "args": [25],
        "className": "ExpBoosterModifier",
        "player": True,
        "stackCount": 99 if stack > 99 else stack,
        "typeId": "EXP_CHARM"
    }
    add_or_update_modifier(existing_data, modifier, "EXP Charm", slot)

def SUPER_EXP_CHARM(existing_data, stack, slot):
    modifier = {
        "args": [60],
        "className": "ExpBoosterModifier",
        "player": True,
        "stackCount": 30 if stack > 30 else stack,
        "typeId": "SUPER_EXP_CHARM"
    }
    add_or_update_modifier(existing_data, modifier, "Super EXP Charm", slot)

def GOLDEN_EXP_CHARM(existing_data, stack, slot):
    modifier = {
        "args": [100],
        "className": "ExpBoosterModifier",
        "player": True,
        "stackCount": 10 if stack > 10 else stack,
        "typeId": "GOLDEN_EXP_CHARM",
    }
    add_or_update_modifier(existing_data, modifier, "Golden EXP Charm", slot)

def HEALING_CHARM(existing_data, stack, slot):
    modifier = {
        "args": [1.1],
        "className": "HealingBoosterModifier",
        "player": True,
        "stackCount": 5 if stack > 5 else stack,
        "typeId": "HEALING_CHARM",
    }
    add_or_update_modifier(existing_data, modifier, "Healing Booster Modifier", slot)

def LOCK_CAPSULE(existing_data, stack, slot):
    modifier = {
        "args": None,
        "className": "LockModifierTiersModifier",
        "player": True,
        "stackCount": 1 if stack > 1 else stack,
        "typeId": "LOCK_CAPSULE",
    }
    add_or_update_modifier(existing_data, modifier, "Lock Modifier Tiers Modifier", slot)

def EXP_BALANCE(existing_data, stack, slot):
    modifier = {
        "args": None,
        "className": "ExpBalanceModifier",
        "player": True,
        "stackCount": 4 if stack > 4 else stack,
        "typeId": "EXP_BALANCE"
    }
    add_or_update_modifier(existing_data, modifier, "EXP Balance Modifier", slot)

def CANDY_JAR(existing_data, stack, slot):
    modifier = {
        "args": None,
        "className": "LevelIncrementBoosterModifier",
        "player": True,
        "stackCount": 99 if stack > 99 else stack,
        "typeId": "CANDY_JAR"
    }
    add_or_update_modifier(existing_data, modifier, "Level Increment Booster Modifier", slot)

def AMULET_COIN(existing_data, stack, slot):
    modifier = {
        "args": None,
        "className": "MoneyMultiplierModifier",
        "player": True,
        "stackCount": 5 if stack > 5 else stack,
        "typeId": "AMULET_COIN"
    }
    add_or_update_modifier(existing_data, modifier, "Money Multiplier Modifier", slot)

def BERRY_POUCH(existing_data, stack, slot):
    modifier = {
        "args": None,
        "className": "PreserveBerryModifier",
        "player": True,
        "stackCount": 3 if stack > 3 else stack,
        "typeId": "BERRY_POUCH"
    }
    add_or_update_modifier(existing_data, modifier, "Preserve Berry Modifier", slot)

def SHELL_BELL(existing_data, stack, slot):
    poke_id = existing_data['party'][slot]['id']
    modifier = {
        "args": [poke_id],
        "className": "HitHealModifier",
        "player": True,
        "stackCount": 9 if stack > 9 else stack,
        "typeId": "SHELL_BELL",
    }
    add_or_update_modifier(existing_data, modifier, "Hit Heal Modifier", slot)

def SOUL_DEW(existing_data, stack, slot):
    poke_id = existing_data['party'][slot]['id']
    modifier = {
        "args": [poke_id],
        "className": "PokemonNatureWeightModifier",
        "player": True,
        "stackCount": 10 if stack > 10 else stack,
        "typeId": "SOUL_DEW"
    }
    add_or_update_modifier(existing_data, modifier, "Pokemon Nature Weight Modifier", slot)


def GRIP_CLAW(existing_data, stack, slot):
    poke_id = existing_data['party'][slot]['id']
    modifier = {
        "args": [poke_id, '10'],
        "className": "ContactHeldItemTransferChanceModifier",
        "player": True,
        "stackCount": 5 if stack > 5 else stack,
        "typeId": "GRIP_CLAW",
    }
    add_or_update_modifier(existing_data, modifier, "Contact Held Item Transfer Chance Modifier", slot)

def GOLDEN_PUNCH(existing_data, stack, slot):
    poke_id = existing_data['party'][slot]['id']
    modifier = {
        "args": [poke_id],
        "className": "DamageMoneyRewardModifier",
        "player": True,
        "stackCount": 5 if stack > 5 else stack,
        "typeId": "GOLDEN_PUNCH",
    }
    add_or_update_modifier(existing_data, modifier, "Damage Money Reward Modifier", slot)

def MINI_BLACK_HOLE(existing_data, stack, slot):
    poke_id = existing_data['party'][slot]['id']
    modifier = {
        "args": [poke_id],
        "className": "TurnHeldItemTransferModifier",
        "player": True,
        "stackCount": 1 if stack > 1 else stack,
        "typeId": "MINI_BLACK_HOLE",
    }
    add_or_update_modifier(existing_data, modifier, "Turn Held Item Transfer Modifier", slot)

def MULTI_LENS(existing_data, stack, slot):
    poke_id = existing_data['party'][slot]['id']
    modifier = {
        "args": [poke_id],
        "className": "PokemonMultiHitModifier",
        "player": True,
        "stackCount": 3 if stack > 3 else stack,
        "typeId": "MULTI_LENS",
    }
    add_or_update_modifier(existing_data, modifier, "Pokemon Multi-Hit Modifier", slot)

def REVIVER_SEED(existing_data, stack, slot):
    poke_id = existing_data['party'][slot]['id']
    modifier = {
        "args": [poke_id],
        "className": "PokemonInstantReviveModifier",
        "player": True,
        "stackCount": 1 if stack > 1 else stack,
        "typeId": "REVIVER_SEED",
    }
    add_or_update_modifier(existing_data, modifier, "Pokemon Instant Revive Modifier", slot)

def print_modifiers(existing_data):
    print(json.dumps(existing_data['modifiers'], indent=4))
    return

def do_all_modifiers(existing_data, stack, slot):
    ABILITY_CHARM(existing_data, stack, slot)
    SHINY_CHARM(existing_data, stack, slot)
    EXP_CHARM(existing_data, stack, slot)
    SUPER_EXP_CHARM(existing_data, stack, slot)
    GOLDEN_EXP_CHARM(existing_data, stack, slot)
    HEALING_CHARM(existing_data, stack, slot)
    MINI_BLACK_HOLE(existing_data, stack, slot)
    MULTI_LENS(existing_data, stack, slot)
    REVIVER_SEED(existing_data, stack, slot)
    LOCK_CAPSULE(existing_data, stack, slot)
    GRIP_CLAW(existing_data, stack, slot)
    GOLDEN_PUNCH(existing_data, stack, slot)
    EXP_BALANCE(existing_data, stack, slot)
    CANDY_JAR(existing_data, stack, slot)
    AMULET_COIN(existing_data, stack, slot)
    BERRY_POUCH(existing_data, stack, slot)
    SHELL_BELL(existing_data, stack, slot)
    SOUL_DEW(existing_data, stack, slot)

# Example usage
if __name__ == "__main__":
    user_menu()
