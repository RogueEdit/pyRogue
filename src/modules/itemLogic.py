import json
from utilities import cFormatter, Color
from colorama import Fore, Style
from enum import Enum
from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class Modifier:
    args: Optional[List[Any]]
    className: str
    player: bool
    stackCount: int
    typeId: str
    typePregenArgs: Optional[List[Any]] = None

class ModifierType(Enum):
    ABILITY_CHARM = Modifier(args=None, className="HiddenAbilityRateBoosterModifier", player=True, stackCount=1, typeId="ABILITY_CHARM")
    SHINY_CHARM = Modifier(args=None, className="ShinyRateBoosterModifier", player=True, stackCount=1, typeId="SHINY_CHARM")
    EXP_CHARM = Modifier(args=[25], className="ExpBoosterModifier", player=True, stackCount=1, typeId="EXP_CHARM")
    SUPER_EXP_CHARM = Modifier(args=[60], className="ExpBoosterModifier", player=True, stackCount=1, typeId="SUPER_EXP_CHARM")
    GOLDEN_EXP_CHARM = Modifier(args=[100], className="ExpBoosterModifier", player=True, stackCount=1, typeId="GOLDEN_EXP_CHARM")
    HEALING_CHARM = Modifier(args=[1.1], className="HealingBoosterModifier", player=True, stackCount=1, typeId="HEALING_CHARM")
    MINI_BLACK_HOLE = Modifier(args=[None], className="TurnHeldItemTransferModifier", player=True, stackCount=1, typeId="MINI_BLACK_HOLE")
    MULTI_LENS = Modifier(args=[None], className="PokemonMultiHitModifier", player=True, stackCount=1, typeId="MULTI_LENS")
    REVIVER_SEED = Modifier(args=[None], className="PokemonInstantReviveModifier", player=True, stackCount=1, typeId="REVIVER_SEED")
    LOCK_CAPSULE = Modifier(args=None, className="LockModifierTiersModifier", player=True, stackCount=1, typeId="LOCK_CAPSULE")
    GRIP_CLAW = Modifier(args=[None, 10], className="ContactHeldItemTransferChanceModifier", player=True, stackCount=1, typeId="GRIP_CLAW")
    GOLDEN_PUNCH = Modifier(args=[None], className="DamageMoneyRewardModifier", player=True, stackCount=1, typeId="GOLDEN_PUNCH")
    EXP_BALANCE = Modifier(args=None, className="ExpBalancerModifier", player=True, stackCount=1, typeId="EXP_BALANCE")
    CANDY_JAR = Modifier(args=None, className="LevelIncrementBoosterModifier", player=True, stackCount=1, typeId="CANDY_JAR")
    AMULET_COIN = Modifier(args=None, className="MoneyMultiplierModifier", player=True, stackCount=1, typeId="AMULET_COIN")
    BERRY_POUCH = Modifier(args=None, className="PreserveBerryModifier", player=True, stackCount=1, typeId="BERRY_POUCH")
    SHELL_BELL = Modifier(args=[None], className="HitHealModifier", player=True, stackCount=1, typeId="SHELL_BELL")
    SOUL_DEW = Modifier(args=[None], className="PokemonNatureWeightModifier", player=True, stackCount=1, typeId="SOUL_DEW")
    WIDE_LENS = Modifier(args=[None], className="PokemonMoveAccuracyBoosterModifier", player=True, stackCount=1, typeId="WIDE_LENS")
    ATTACK_TYPE_BOOSTER = Modifier(args=[None, 14, 20], className="AttackTypeBoosterModifier", player=True, stackCount=1, typeId="ATTACK_TYPE_BOOSTER", typePregenArgs=[14])

class ModifierEditor:

    def __init__(self):
        self.menu_items = self.create_menu_items()

    def create_menu_items(self):
        menu_items = [("\npyRogue Item Editor", 'title')]
        for mod_type in ModifierType:
            mod_name = mod_type.value.className.replace(' ', '')  # Ensure no spaces in className
            menu_items.append(((mod_name, mod_type.value.typeId), mod_type))
            
        menu_items.append(("pyRogue Item Editor", 'category'))
        menu_items.append((("Apply All Modifiers", "Give All"), self.do_all_modifiers))
        menu_items.append((('Return to Main Menu', f'{Fore.LIGHTYELLOW_EX}Use when done'), self.end))
        menu_items.append(("pyRogue Item Editor", 'title'))
        return menu_items

    @staticmethod
    def format_modifier_name(name):
        return ' '.join([word.capitalize() for word in name.split('_')])

    @staticmethod
    def load_json(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    @staticmethod
    def save_json(data, file_path):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def ensure_modifiers_block(data, type_id):
        if 'modifiers' not in data or not isinstance(data['modifiers'], list):
            data['modifiers'] = []
        for modifier in data['modifiers']:
            if modifier.get('typeId') == type_id:
                return modifier.get('stackCount', 0)
        return None

    def add_or_update_modifier(self, data, modifier_type: ModifierType, stack, slot, sessionSlot):
        modifier = modifier_type.value
        modifier.stackCount = stack

        # Handle args with poke_id
        poke_id = data['party'][slot]['id']
        if modifier.args:
            modifier.args = [poke_id if arg is None else arg for arg in modifier.args]

        if 'modifiers' not in data or not isinstance(data['modifiers'], list):
            data['modifiers'] = []

        def modifiers_match(existing_modifier, new_modifier):
            if existing_modifier['typeId'] != new_modifier['typeId']:
                return False
            if existing_modifier.get('args') != new_modifier['args']:
                return False
            return True

        existing = next(
            (m for m in data['modifiers'] if modifiers_match(m, modifier.__dict__)),
            None
        )

        if existing:
            existing['stackCount'] = modifier.stackCount
        else:
            data['modifiers'].append(modifier.__dict__)

        self.save_json(data, f'slot_{sessionSlot}.json')
        cFormatter.print(Color.GREEN, f'Successfully added {modifier.stackCount} {modifier.typeId}.')

    def user_menu(self, sessionSlot):

        while True:
            try:
                print('')
                valid_choices = cFormatter.initialize_menu(self.menu_items)
                choice = int(input("Select an option by number: ").strip())
                selected_item = next((item for item in valid_choices if item[0] == choice), None)

                if selected_item is None:
                    cFormatter.print(Color.ERROR, "Invalid choice, please try again.")
                    continue

                chosen_item = selected_item[1]

                if callable(chosen_item):
                    chosen_item(sessionSlot)
                else:
                    selected_modifier = chosen_item
                    party_num = int(input('Select the party slot of the Pokémon you want to edit (0-5): '))
                    if party_num < 0 or party_num > 5:
                        cFormatter.print(Color.ERROR, "Invalid party slot, please try again.")
                        continue

                    existing_data = self.load_json(f'slot_{sessionSlot}.json')
                    stacks_raw = self.ensure_modifiers_block(existing_data, selected_modifier.value.typeId)
                    if stacks_raw:
                        stack_count = int(input(f"You already have {stacks_raw} of {selected_modifier.value.typeId}. Set it to: "))
                    else:
                        stack_count = int(input(f'How many {selected_modifier.value.typeId} do you want?: '))

                    self.add_or_update_modifier(existing_data, selected_modifier, stack_count, party_num, sessionSlot)

            except ValueError:
                cFormatter.print(Color.ERROR, "Invalid input, please enter a number.")

    def do_all_modifiers(self, sessionSlot):
        try:
            party_num = int(input('Select the party slot of the Pokémon you want to edit (0-5): '))
            if party_num < 0 or party_num > 5:
                cFormatter.print(Color.ERROR, "Invalid party slot, please try again.")
                return

            stack_count = int(input('Enter the stack count for the modifiers: '))
            existing_data = self.load_json(f'slot_{sessionSlot}.json')

            for mod_type in ModifierType:
                self.add_or_update_modifier(existing_data, mod_type, stack_count, party_num, sessionSlot)

        except ValueError:
            cFormatter.print(Color.ERROR, "Invalid input, please enter a number.")

    @staticmethod
    def end():
        cFormatter.print(Color.GREEN, "Exiting pyRogue Item Editor.")
        return None

    @staticmethod
    def print_modifiers(sessionSlot):
        data = ModifierEditor.load_json(f'slot_{sessionSlot}.json')
        if 'modifiers' in data and isinstance(data['modifiers'], list):
            cFormatter.print(Color.INFO, "Current Modifiers:")
            for modifier in data['modifiers']:
                cFormatter.print(Color.INFO, json.dumps(modifier, indent=4))
        else:
            cFormatter.print(Color.INFO, "No modifiers found.")