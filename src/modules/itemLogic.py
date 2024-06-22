# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/JulianStiebler/
# Date of release: 13.06.2024 
# Last Edited: 20.06.2024

# Unlike the other code, reusing this in your own project is forbidden.

import json
from utilities import cFormatter, Color
from colorama import Fore
from enum import Enum
from dataclasses import dataclass
from typing import Any, List, Optional
from modules.config import version

@dataclass
class Modifier:
    args: Optional[List[Any]]
    className: str
    player: bool
    stackCount: int
    typeId: str
    typePregenArgs: Optional[List[Any]] = None

class ModifierType(Enum):
    ABILITY_CHARM = Modifier(args=None, className='HiddenAbilityRateBoosterModifier', player=True, stackCount=1, typeId='ABILITY_CHARM')
    AMULET_COIN = Modifier(args=None, className='MoneyMultiplierModifier', player=True, stackCount=1, typeId='AMULET_COIN')
    SILK_SCARF = Modifier(args=[None, 0, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[0])
    BLACK_BELT = Modifier(args=[None, 1, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[1])
    SHARP_BEAK = Modifier(args=[None, 2, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[2])
    POISON_BARB = Modifier(args=[None, 3, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[3])
    SOFT_SAND = Modifier(args=[None, 4, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[4])
    HARD_STONE = Modifier(args=[None, 5, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[5])
    SILVER_POWDER = Modifier(args=[None, 6, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[6])
    SPELL_TAG = Modifier(args=[None, 7, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[7])
    METAL_COAT = Modifier(args=[None, 8, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[8])
    CHARCOAL = Modifier(args=[None, 9, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[9])
    MYSTIC_WATER = Modifier(args=[None, 10, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[10])
    MIRACLE_SEED = Modifier(args=[None, 11, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[11])
    MAGNET = Modifier(args=[None, 12, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[12])
    TWISTED_SPOON = Modifier(args=[None, 13, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[13])
    NEVER_MELT_ICE = Modifier(args=[None, 14, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[14])
    DRAGON_FANG = Modifier(args=[None, 15, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[15])
    BLACK_GLASSES = Modifier(args=[None, 16, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[16])
    FAIRY_FEATHER = Modifier(args=[None, 17, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[17])
    PROTEIN = Modifier(args=[None, 1], className='PokemonBaseStatModifier', player=True, stackCount=1, typeId='BASE_STAT_BOOSTER', typePregenArgs=[1])
    IRON = Modifier(args=[None, 2], className='PokemonBaseStatModifier', player=True, stackCount=1, typeId='BASE_STAT_BOOSTER', typePregenArgs=[2])
    CALCIUM = Modifier(args=[None, 3], className='PokemonBaseStatModifier', player=True, stackCount=1, typeId='BASE_STAT_BOOSTER', typePregenArgs=[3])
    ZINC = Modifier(args=[None, 4], className='PokemonBaseStatModifier', player=True, stackCount=1, typeId='BASE_STAT_BOOSTER', typePregenArgs=[4])
    CARBOS = Modifier(args=[None, 5], className='PokemonBaseStatModifier', player=True, stackCount=1, typeId='BASE_STAT_BOOSTER', typePregenArgs=[5])
    SITRUS_BERRY = Modifier(args=[None, 0], className='BerryModifier', player=True, stackCount=1, typeId='BERRY', typePregenArgs=[0]) 
    LUM_BERRY = Modifier(args=[None, 1], className='BerryModifier', player=True, stackCount=1, typeId='BERRY', typePregenArgs=[1]) 
    ENIGMA_BERRY = Modifier(args=[None, 2], className='BerryModifier', player=True, stackCount=1, typeId='BERRY', typePregenArgs=[2]) # Max 2
    LIECHI_BERRY = Modifier(args=[None, 3], className='BerryModifier', player=True, stackCount=1, typeId='BERRY', typePregenArgs=[3])
    GANLON_BERRY = Modifier(args=[None, 4], className='BerryModifier', player=True, stackCount=1, typeId='BERRY', typePregenArgs=[4])
    PETAYA_BERRY = Modifier(args=[None, 5], className='BerryModifier', player=True, stackCount=1, typeId='BERRY', typePregenArgs=[5])
    APICOT_BERRY = Modifier(args=[None, 6], className='BerryModifier', player=True, stackCount=1, typeId='BERRY', typePregenArgs=[6])
    SALAC_BERRY = Modifier(args=[None, 7], className='BerryModifier', player=True, stackCount=1, typeId='BERRY', typePregenArgs=[7])
    LANSAT_BERRY = Modifier(args=[None, 8], className='BerryModifier', player=True, stackCount=1, typeId='BERRY', typePregenArgs=[8])
    STARF_BERRY = Modifier(args=[None, 9], className='BerryModifier', player=True, stackCount=1, typeId='BERRY', typePregenArgs=[9])
    LEPPA_BERRY = Modifier(args=[None, 10], className='BerryModifier', player=True, stackCount=1, typeId='BERRY', typePregenArgs=[10])
    BERRY_POUCH = Modifier(args=None, className='PreserveBerryModifier', player=True, stackCount=1, typeId='BERRY_POUCH')
    CANDY_JAR = Modifier(args=None, className='LevelIncrementBoosterModifier', player=True, stackCount=1, typeId='CANDY_JAR')
    DYNAMAX_BAND = Modifier(args=None, className='GigantamaxAccessModifier', player=True, stackCount=1, typeId='DYNAMAX_BAND')
    EXP_BALANCE = Modifier(args=None, className='ExpBalanceModifier', player=True, stackCount=1, typeId='EXP_BALANCE')
    EXP_CHARM = Modifier(args=[25], className='ExpBoosterModifier', player=True, stackCount=1, typeId='EXP_CHARM')
    EXP_SHARE = Modifier(args=None, className='ExpShareModifier', player=True, stackCount=1, typeId='EXP_SHARE')
    FOCUS_BAND = Modifier(args=[None], className='SurviveDamageModifier', player=True, stackCount=1, typeId='FOCUS_BAND')
    FORM_CHANGE_ITEM = Modifier(args=[None, None, True], className='PokemonFormChangeItemModifier', player=True, stackCount=1, typeId='FORM_CHANGE_ITEM', typePregenArgs=[None])
    GOLDEN_EGG = Modifier(args=[None, None], className='PokemonExpBoosterModifier', player=True, stackCount=1, typeId='GOLDEN_EGG')
    GOLDEN_POKEBALL = Modifier(args=None, className='ExtraModifierModifier', player=True, stackCount=1, typeId='GOLDEN_POKEBALL')
    GOLDEN_PUNCH = Modifier(args=[None], className='DamageMoneyRewardModifier', player=True, stackCount=1, typeId='GOLDEN_PUNCH')
    GRIP_CLAW = Modifier(args=[None, 10], className='ContactHeldItemTransferChanceModifier', player=True, stackCount=1, typeId='GRIP_CLAW')
    HEALING_CHARM = Modifier(args=[1.1], className='HealingBoosterModifier', player=True, stackCount=1, typeId='HEALING_CHARM')
    IV_SCANNER = Modifier(args=None, className='IvScannerModifier', player=True, stackCount=1, typeId='IV_SCANNER')
    KINGS_ROCK = Modifier(args=[None], className='FlinchChanceModifier', player=True, stackCount=1, typeId='KINGS_ROCK')
    LEFTOVERS = Modifier(args=[None], className='TurnHealModifier', player=True, stackCount=1, typeId='LEFTOVERS')
    LOCK_CAPSULE = Modifier(args=None, className='LockModifierTiersModifier', player=True, stackCount=1, typeId='LOCK_CAPSULE')
    LUCKY_EGG = Modifier(args=[None, None], className='PokemonExpBoosterModifier', player=True, stackCount=1, typeId='LUCKY_EGG')
    MEGA_BRACELET = Modifier(args=None, className='MegaEvolutionAccessModifier', player=True, stackCount=1, typeId='MEGA_BRACELET')
    MINI_BLACK_HOLE = Modifier(args=[None], className='TurnHeldItemTransferModifier', player=True, stackCount=1, typeId='MINI_BLACK_HOLE')
    MULTI_LENS = Modifier(args=[None], className='PokemonMultiHitModifier', player=True, stackCount=1, typeId='MULTI_LENS')
    QUICK_CLAW = Modifier(args=[None], className='BypassSpeedChanceModifier', player=True, stackCount=1, typeId='QUICK_CLAW')
    REVIVER_SEED = Modifier(args=[None], className='PokemonInstantReviveModifier', player=True, stackCount=1, typeId='REVIVER_SEED')
    SHELL_BELL = Modifier(args=[None], className='HitHealModifier', player=True, stackCount=1, typeId='SHELL_BELL')
    SHINY_CHARM = Modifier(args=None, className='ShinyRateBoosterModifier', player=True, stackCount=1, typeId='SHINY_CHARM')
    SOOTHE_BELL = Modifier(args=[None], className='PokemonFriendshipBoosterModifier', player=True, stackCount=1, typeId='SOOTHE_BELL')
    SOUL_DEW = Modifier(args=[None], className='PokemonNatureWeightModifier', player=True, stackCount=1, typeId='SOUL_DEW')
    SUPER_EXP_CHARM = Modifier(args=[None], className='ExpBoosterModifier', player=True, stackCount=1, typeId='SUPER_EXP_CHARM')
    WIDE_LENS = Modifier(args=[None, 5], className='PokemonMoveAccuracyBoosterModifier', player=True, stackCount=1, typeId='WIDE_LENS')
    X_ATTACK = Modifier(args=[0, 5], className='TempBattleStatBoosterModifier', player=True, stackCount=1, typeId='TEMP_STAT_BOOSTER', typePregenArgs=[0])
    X_DEFENSE = Modifier(args=[1, 5], className='TempBattleStatBoosterModifier', player=True, stackCount=1, typeId='TEMP_STAT_BOOSTER', typePregenArgs=[1])
    X_SP_ATK = Modifier(args=[2, 5], className='TempBattleStatBoosterModifier', player=True, stackCount=1, typeId='TEMP_STAT_BOOSTER', typePregenArgs=[2])
    X_SP_DEF = Modifier(args=[3, 5], className='TempBattleStatBoosterModifier', player=True, stackCount=1, typeId='TEMP_STAT_BOOSTER', typePregenArgs=[3])
    X_SPEED = Modifier(args=[4, 5], className='TempBattleStatBoosterModifier', player=True, stackCount=1, typeId='TEMP_STAT_BOOSTER', typePregenArgs=[4])
    X_ACCURACY = Modifier(args=[5, 5], className='TempBattleStatBoosterModifier', player=True, stackCount=1, typeId='TEMP_STAT_BOOSTER', typePregenArgs=[5])
    X_DIRE_HIT = Modifier(args=[6, 5], className='TempBattleStatBoosterModifier', player=True, stackCount=1, typeId='TEMP_STAT_BOOSTER', typePregenArgs=[6])

class ModifierEditor:
    def __init__(self):
        self.menu_items = self.create_menu_items()

    def create_menu_items(self):
        menu_items = [(f"\n{version}", 'title')]
        for mod_type in ModifierType:
            # Extracting the ModifierType name
            mod_name = mod_type.name
            modifier = mod_type.value
            # Combining typeId with typePregenArgs if present
            type_info = modifier.typeId
            if modifier.typePregenArgs:
                type_info += f" ({', '.join(map(str, modifier.typePregenArgs))})"
            # Appending to menu_items
            menu_items.append(((mod_name, type_info), mod_type))

        menu_items.append(("pyRogue Item Editor", 'category'))
        menu_items.append((("Give all Modifiers", "Give All"), self.do_all_modifiers))
        menu_items.append((('Return to Main Menu', f'{Fore.LIGHTYELLOW_EX}Use when done'), self.end))
        menu_items.append(("You can save these changed in the Main Menu", 'title'))
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
        cFormatter.print(Color.GREEN, f'Successfully written {modifier.stackCount} {modifier.typeId} to slot_{sessionSlot}.')

    def user_menu(self, sessionSlot):

        existing_data = self.load_json(f'slot_{sessionSlot}.json')
        while True:
            if existing_data['gameMode'] == 3:
                cFormatter.print(Color.CRITICAL, 'Cannot edit items on daily runs!')
                break
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
                    if chosen_item == self.end:
                        chosen_item()
                        break
                    else:
                        chosen_item(sessionSlot)
                else:
                    selected_modifier = chosen_item
                    party_num = int(input('Select the party slot of the Pokémon you want to edit (0-5): '))
                    if party_num < 0 or party_num > 5:
                        cFormatter.print(Color.ERROR, "Invalid party slot, please try again.")
                        continue

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
            try:
                for mod_type in ModifierType:
                    self.add_or_update_modifier(existing_data, mod_type, stack_count, party_num, sessionSlot)
            except Exception as e:
                cFormatter.print(Color.WARNING, f'Something unexpected happened. {e}', isLogging=True)

        except ValueError:
            cFormatter.print(Color.ERROR, "Invalid input, please enter a number.")

    @staticmethod
    def end():
        cFormatter.print(Color.GREEN, "Leaving pyRogue Item Editor.")

    @staticmethod
    def print_modifiers(sessionSlot):
        data = ModifierEditor.load_json(f'slot_{sessionSlot}.json')
        if 'modifiers' in data and isinstance(data['modifiers'], list):
            cFormatter.print(Color.INFO, "Current Modifiers:")
            for modifier in data['modifiers']:
                cFormatter.print(Color.INFO, json.dumps(modifier, indent=4))
        else:
            cFormatter.print(Color.INFO, "No modifiers found.")