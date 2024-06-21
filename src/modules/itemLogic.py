import json
from utilities import cFormatter, Color
from colorama import Fore, Style

class ModifierEditor:
    """
    ModifierEditor allows the user to edit item modifiers for a game.

    Attributes:
        menu_items (list): A list of menu items and associated functions.
    """

    def __init__(self):
        self.menu_items = [
            ("pyRogue Item Editor", 'title'),
            (("Hidden Ability Rate Booster Modifier", 'Ability Charm'), self.ABILITY_CHARM),
            (("Shiny Rate Booster Modifier", 'Shiny Charm'), self.SHINY_CHARM),
            (("EXP Charm", 'EXP Charm'), self.EXP_CHARM),
            (("Super EXP Charm", 'Super EXP Charm'), self.SUPER_EXP_CHARM),
            (("Golden EXP Charm", 'Gold EXP Charm'), self.GOLDEN_EXP_CHARM),
            (("Healing Booster Modifier", 'Healing Charm'), self.HEALING_CHARM),
            (("On-hit item stealer", 'Mini Black Hole'), self.MINI_BLACK_HOLE),
            (("Multi-Hit Modifier", 'Multi Lens'), self.MULTI_LENS),
            (("On-death revive", 'Reviver Seed'), self.REVIVER_SEED),
            (("Lock Capsule", 'Lock Capsule'), self.LOCK_CAPSULE),
            (("On-hit item stealer", 'Grip Claw'), self.GRIP_CLAW),
            (("On-hit money rewarded", 'Golden Punch'), self.GOLDEN_PUNCH),
            (("EXP Balancer", 'EXP Balance'), self.EXP_BALANCE),
            (("Rare Candy Booster", 'Candy Jar'), self.CANDY_JAR),
            (("More money from trainers", 'Amulet Coin'), self.AMULET_COIN),
            (("Chance to not lose berries", 'Berry Pouch'), self.BERRY_POUCH),
            (("Heal-on-hit", 'Shell Bell'), self.SHELL_BELL),
            (("Pokemon Nature Weight Modifier", 'Soul Dew'), self.SOUL_DEW),
            (('Give all listed', 'Give all :)'), self.do_all_modifiers),
            (("Print Modifiers", ''), self.print_modifiers),
            (("Return to Menu", f'{Fore.LIGHTYELLOW_EX} When done use this then save {Style.RESET_ALL}'), self.end),
            ("pyRogue Item Editor", 'title'),
        ]

    @staticmethod
    def end():
        """
        Ends the current operation and returns None.

        :return: None
        """
        return None

    @staticmethod
    def load_json(file_path):
        """
        Loads JSON data from a specified file.

        :param file_path: Path to the JSON file.
        :type file_path: str
        :return: Data loaded from the JSON file.
        :rtype: dict
        """
        with open(file_path, 'r') as file:
            return json.load(file)

    @staticmethod
    def save_json(data, file_path):
        """
        Saves data to a specified JSON file.

        :param data: Data to be saved.
        :type data: dict
        :param file_path: Path to the JSON file.
        :type file_path: str
        """
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def ensure_modifiers_block(data, type_id):
        """
        Ensures the 'modifiers' block is present and returns the stack count for the given type_id.

        :param data: Data to be checked and modified.
        :type data: dict
        :param type_id: The type ID of the modifier.
        :type type_id: str
        :return: The stack count for the given type_id, or None if not found.
        :rtype: int or None
        """
        if 'modifiers' not in data or not isinstance(data['modifiers'], list):
            data['modifiers'] = []

        for modifier in data['modifiers']:
            if modifier.get('typeId') == type_id:
                return modifier.get('stackCount', 0)
        return None

    @staticmethod
    def add_or_update_modifier(data, modifier, modifier_name, slot, sessionSlot):
        """
        Adds or updates a modifier in the data.

        :param data: Data to be modified.
        :type data: dict
        :param modifier: Modifier to be added or updated.
        :type modifier: dict
        :param modifier_name: Name of the modifier.
        :type modifier_name: str
        :param slot: Slot number for the modifier.
        :type slot: int
        :param sessionSlot: Session slot number for saving the data.
        :type sessionSlot: int
        """
        def modifiers_match(existing_modifier, new_modifier):
            if existing_modifier['typeId'] != new_modifier['typeId']:
                return False
            if existing_modifier.get('args') != new_modifier.get('args'):
                return False
            return True

        existing = next(
            (m for m in data['modifiers'] if modifiers_match(m, modifier)),
            None
        )

        if existing:
            existing['stackCount'] = modifier['stackCount']
        else:
            data['modifiers'].append(modifier)

        ModifierEditor.save_json(data, f'slot_{sessionSlot}.json')
        cFormatter.print(Color.GREEN, f'Successfully added {modifier["stackCount"]} {modifier_name}.')
        cFormatter.print(Color.INFO, 'Some items are limited, hence why it didn\'t apply all you may wanted.')

    def user_menu(self, sessionSlot):
        """
        Displays the user menu for item editing.

        :param sessionSlot: Session slot number.
        :type sessionSlot: int
        """
        try:
            while True:
                existing_data = self.load_json(f'slot_{sessionSlot}.json')
                valid_choices = cFormatter.initialize_menu(self.menu_items)
                user_input = input("Command: ").strip().lower()
                if user_input == 'exit':
                    raise KeyboardInterrupt  # Raise KeyboardInterrupt to exit the program

                if user_input.isdigit():
                    choice_index = int(user_input)
                    for idx, func in valid_choices:
                        if idx == choice_index:
                            function_name = func.__name__
                            if function_name == 'print_modifiers':
                                self.print_modifiers(existing_data)
                                break

                            if function_name == 'end':
                                return

                            slot = int(input('Select the Pokemon slot you want to edit (0-5): '))
                            if slot < 0 or slot > 5:
                                print('Invalid session slot.')
                                continue

                            if function_name == 'do_all_modifiers':
                                stack = int(input('How many all listed modifiers do you want?: '))
                                self.do_all_modifiers(existing_data, stack, slot, sessionSlot)
                                break

                            stacks_raw = self.ensure_modifiers_block(existing_data, function_name)
                            if stacks_raw:
                                stack = int(input(f"You already have {stacks_raw} of {function_name}. Set it to: "))
                            else:
                                stack = int(input(f'How many {function_name} do you want?: '))

                            func(existing_data, stack, slot, sessionSlot)  # Call the associated function
                            break
                    else:
                        print("Invalid selection. Please choose a valid menu option.")
                else:
                    print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("Program interrupted by user.")

    def ABILITY_CHARM(self, existing_data, stack, slot, sessionSlot):
        """
        Adds or updates the Hidden Ability Rate Booster Modifier.

        :param existing_data: Existing data to be modified.
        :type existing_data: dict
        :param stack: Stack count for the modifier.
        :type stack: int
        :param slot: Slot number for the modifier.
        :type slot: int
        :param sessionSlot: Session slot number for saving the data.
        :type sessionSlot: int
        """
        modifier = {
            "className": "HiddenAbilityRateBoosterModifier",
            "args": None,
            "player": True,
            "stackCount": 10 if stack > 10 else stack,
            "typeId": "ABILITY_CHARM"
        }
        self.add_or_update_modifier(existing_data, modifier, "Hidden Ability Rate Booster Modifier", slot, sessionSlot)

    def SHINY_CHARM(self, existing_data, stack, slot, sessionSlot):
        """
        Adds or updates the Shiny Rate Booster Modifier.

        :param existing_data: Existing data to be modified.
        :type existing_data: dict
        :param stack: Stack count for the modifier.
        :type stack: int
        :param slot: Slot number for the modifier.
        :type slot: int
        :param sessionSlot: Session slot number for saving the data.
        :type sessionSlot: int
        """
        modifier = {
            "args": None,
            "className": "ShinyRateBoosterModifier",
            "player": True,
            "stackCount": 4 if stack > 4 else stack,
            "typeId": "SHINY_CHARM"
        }
        self.add_or_update_modifier(existing_data, modifier, "Shiny Rate Booster Modifier", slot, sessionSlot)

    def EXP_CHARM(self, existing_data, stack, slot, sessionSlot):
        """
        Adds or updates the EXP Charm.

        :param existing_data: Existing data to be modified.
        :type existing_data: dict
        :param stack: Stack count for the modifier.
        :type stack: int
        :param slot: Slot number for the modifier.
        :type slot: int
        :param sessionSlot: Session slot number for saving the data.
        :type sessionSlot: int
        """
        modifier = {
            "args": 1.5,
            "className": "ExpRateModifier",
            "player": True,
            "stackCount": 1 if stack > 1 else stack,
            "typeId": "EXP_CHARM"
        }
        self.add_or_update_modifier(existing_data, modifier, "EXP Charm", slot, sessionSlot)

    def SUPER_EXP_CHARM(self, existing_data, stack, slot, sessionSlot):
        """
        Adds or updates the Super EXP Charm.

        :param existing_data: Existing data to be modified.
        :type existing_data: dict
        :param stack: Stack count for the modifier.
        :type stack: int
        :param slot: Slot number for the modifier.
        :type slot: int
        :param sessionSlot: Session slot number for saving the data.
        :type sessionSlot: int
        """
        modifier = {
            "args": 60,
            "className": "ExpRateModifier",
            "player": True,
            "stackCount": 1 if stack > 1 else stack,
            "typeId": "SUPER_EXP_CHARM"
        }
        self.add_or_update_modifier(existing_data, modifier, "Super EXP Charm", slot, sessionSlot)

    def GOLDEN_EXP_CHARM(self, existing_data, stack, slot, sessionSlot):
        """
        Adds or updates the Golden EXP Charm.

        :param existing_data: Existing data to be modified.
        :type existing_data: dict
        :param stack: Stack count for the modifier.
        :type stack: int
        :param slot: Slot number for the modifier.
        :type slot: int
        :param sessionSlot: Session slot number for saving the data.
        :type sessionSlot: int
        """
        modifier = {
            "args": 100,
            "className": "ExpRateModifier",
            "player": True,
            "stackCount": 1 if stack > 1 else stack,
            "typeId": "GOLDEN_EXP_CHARM"
        }
        self.add_or_update_modifier(existing_data, modifier, "Golden EXP Charm", slot, sessionSlot)

    def HEALING_CHARM(self, existing_data, stack, slot, sessionSlot):
        """
        Adds or updates the Healing Booster Modifier.

        :param existing_data: Existing data to be modified.
        :type existing_data: dict
        :param stack: Stack count for the modifier.
        :type stack: int
        :param slot: Slot number for the modifier.
        :type slot: int
        :param sessionSlot: Session slot number for saving the data.
        :type sessionSlot: int
        """
        modifier = {
            "args": 1.1,
            "className": "HealingRateModifier",
            "player": True,
            "stackCount": 1 if stack > 1 else stack,
            "typeId": "HEALING_CHARM"
        }
        self.add_or_update_modifier(existing_data, modifier, "Healing Booster Modifier", slot, sessionSlot)

    def MINI_BLACK_HOLE(self, existing_data, stack, slot, sessionSlot):
        """
        Adds or updates the On-hit item stealer (Mini Black Hole) modifier.

        :param existing_data: Existing data to be modified.
        :type existing_data: dict
        :param stack: Stack count for the modifier.
        :type stack: int
        :param slot: Slot number for the modifier.
        :type slot: int
        :param sessionSlot: Session slot number for saving the data.
        :type sessionSlot: int
        """
        poke_id = existing_data['party'][slot]['id']
        modifier = {
            "args": [poke_id],
            "className": "ItemStealModifier",
            "player": True,
            "stackCount": 1 if stack > 1 else stack,
            "typeId": "MINI_BLACK_HOLE"
        }
        self.add_or_update_modifier(existing_data, modifier, "Mini Black Hole", slot, sessionSlot)

    def MULTI_LENS(self, existing_data, stack, slot, sessionSlot):
        """
        Adds or updates the Multi-Hit Modifier (Multi Lens).

        :param existing_data: Existing data to be modified.
        :type existing_data: dict
        :param stack: Stack count for the modifier.
        :type stack: int
        :param slot: Slot number for the modifier.
        :type slot: int
        :param sessionSlot: Session slot number for saving the data.
        :type sessionSlot: int
        """
        poke_id = existing_data['party'][slot]['id']
        modifier = {
            "args": [poke_id],
            "className": "MultiHitModifier",
            "player": True,
            "stackCount": 1 if stack > 1 else stack,
            "typeId": "MULTI_LENS"
        }
        self.add_or_update_modifier(existing_data, modifier, "Multi Lens", slot, sessionSlot)

    def REVIVER_SEED(self, existing_data, stack, slot, sessionSlot):
        """
        Adds or updates the On-death revive (Reviver Seed) modifier.

        :param existing_data: Existing data to be modified.
        :type existing_data: dict
        :param stack: Stack count for the modifier.
        :type stack: int
        :param slot: Slot number for the modifier.
        :type slot: int
        :param sessionSlot: Session slot number for saving the data.
        :type sessionSlot: int
        """
        poke_id = existing_data['party'][slot]['id']
        modifier = {
            "args": [poke_id],
            "className": "ReviveModifier",
            "player": True,
            "stackCount": 1 if stack > 1 else stack,
            "typeId": "REVIVER_SEED"
        }
        self.add_or_update_modifier(existing_data, modifier, "Reviver Seed", slot, sessionSlot)

    def LOCK_CAPSULE(self, existing_data, stack, slot, sessionSlot):
        """
        Adds or updates the Lock Capsule modifier.

        :param existing_data: Existing data to be modified.
        :type existing_data: dict
        :param stack: Stack count for the modifier.
        :type stack: int
        :param slot: Slot number for the modifier.
        :type slot: int
        :param sessionSlot: Session slot number for saving the data.
        :type sessionSlot: int
        """
        modifier = {
            "args": None,
            "className": "LockModifier",
            "player": True,
            "stackCount": 1 if stack > 1 else stack,
            "typeId": "LOCK_CAPSULE"
        }
        self.add_or_update_modifier(existing_data, modifier, "Lock Capsule", slot, sessionSlot)

    def GRIP_CLAW(self, existing_data, stack, slot, sessionSlot):
        """
        Adds or updates the On-hit item stealer (Grip Claw) modifier.

        :param existing_data: Existing data to be modified.
        :type existing_data: dict
        :param stack: Stack count for the modifier.
        :type stack: int
        :param slot: Slot number for the modifier.
        :type slot: int
        :param sessionSlot: Session slot number for saving the data.
        :type sessionSlot: int
        """
        poke_id = existing_data['party'][slot]['id']
        modifier = {
            "args": [poke_id, 10],
            "className": "ItemStealModifier",
            "player": True,
            "stackCount": 1 if stack > 1 else stack,
            "typeId": "GRIP_CLAW"
        }
        self.add_or_update_modifier(existing_data, modifier, "Grip Claw", slot, sessionSlot)

    def GOLDEN_PUNCH(self, existing_data, stack, slot, sessionSlot):
        """
        Adds or updates the On-hit money rewarded (Golden Punch) modifier.

        :param existing_data: Existing data to be modified.
        :type existing_data: dict
        :param stack: Stack count for the modifier.
        :type stack: int
        :param slot: Slot number for the modifier.
        :type slot: int
        :param sessionSlot: Session slot number for saving the data.
        :type sessionSlot: int
        """
        poke_id = existing_data['party'][slot]['id']
        modifier = {
            "args": [poke_id],
            "className": "MoneyRewardModifier",
            "player": True,
            "stackCount": 1 if stack > 1 else stack,
            "typeId": "GOLDEN_PUNCH"
        }
        self.add_or_update_modifier(existing_data, modifier, "Golden Punch", slot, sessionSlot)

    def EXP_BALANCE(self, existing_data, stack, slot, sessionSlot):
        """
        Adds or updates the EXP Balancer.

        :param existing_data: Existing data to be modified.
        :type existing_data: dict
        :param stack: Stack count for the modifier.
        :type stack: int
        :param slot: Slot number for the modifier.
        :type slot: int
        :param sessionSlot: Session slot number for saving the data.
        :type sessionSlot: int
        """
        modifier = {
            "args": None,
            "className": "ExpBalancerModifier",
            "player": True,
            "stackCount": 1 if stack > 1 else stack,
            "typeId": "EXP_BALANCE"
        }
        self.add_or_update_modifier(existing_data, modifier, "EXP Balancer", slot, sessionSlot)

    def CANDY_JAR(self, existing_data, stack, slot, sessionSlot):
        """
        Adds or updates the Rare Candy Booster (Candy Jar) modifier.

        :param existing_data: Existing data to be modified.
        :type existing_data: dict
        :param stack: Stack count for the modifier.
        :type stack: int
        :param slot: Slot number for the modifier.
        :type slot: int
        :param sessionSlot: Session slot number for saving the data.
        :type sessionSlot: int
        """
        modifier = {
            "args": None,
            "className": "LevelIncrementModifier",
            "player": True,
            "stackCount": 99 if stack > 99 else stack,
            "typeId": "CANDY_JAR"
        }
        self.add_or_update_modifier(existing_data, modifier, "Candy Jar", slot, sessionSlot)

    def AMULET_COIN(self, existing_data, stack, slot, sessionSlot):
        """
        Adds or updates the More Money from Trainers (Amulet Coin) modifier.

        :param existing_data: Existing data to be modified.
        :type existing_data: dict
        :param stack: Stack count for the modifier.
        :type stack: int
        :param slot: Slot number for the modifier.
        :type slot: int
        :param sessionSlot: Session slot number for saving the data.
        :type sessionSlot: int
        """
        modifier = {
            "args": None,
            "className": "MoneyMultiplierModifier",
            "player": True,
            "stackCount": 5 if stack > 5 else stack,
            "typeId": "AMULET_COIN"
        }
        self.add_or_update_modifier(existing_data, modifier, "Amulet Coin", slot, sessionSlot)

    def BERRY_POUCH(self, existing_data, stack, slot, sessionSlot):
        """
        Adds or updates the Chance to Not Lose Berries (Berry Pouch) modifier.

        :param existing_data: Existing data to be modified.
        :type existing_data: dict
        :param stack: Stack count for the modifier.
        :type stack: int
        :param slot: Slot number for the modifier.
        :type slot: int
        :param sessionSlot: Session slot number for saving the data.
        :type sessionSlot: int
        """
        modifier = {
            "args": None,
            "className": "BerryPreserveModifier",
            "player": True,
            "stackCount": 3 if stack > 3 else stack,
            "typeId": "BERRY_POUCH"
        }
        self.add_or_update_modifier(existing_data, modifier, "Berry Pouch", slot, sessionSlot)

    def SHELL_BELL(self, existing_data, stack, slot, sessionSlot):
        """
        Adds or updates the Heal-on-Hit (Shell Bell) modifier.

        :param existing_data: Existing data to be modified.
        :type existing_data: dict
        :param stack: Stack count for the modifier.
        :type stack: int
        :param slot: Slot number for the modifier.
        :type slot: int
        :param sessionSlot: Session slot number for saving the data.
        :type sessionSlot: int
        """
        poke_id = existing_data['party'][slot]['id']
        modifier = {
            "args": [poke_id],
            "className": "HitHealModifier",
            "player": True,
            "stackCount": 9 if stack > 9 else stack,
            "typeId": "SHELL_BELL"
        }
        self.add_or_update_modifier(existing_data, modifier, "Shell Bell", slot, sessionSlot)

    def SOUL_DEW(self, existing_data, stack, slot, sessionSlot):
        """
        Adds or updates the Pokemon Nature Weight Modifier (Soul Dew).

        :param existing_data: Existing data to be modified.
        :type existing_data: dict
        :param stack: Stack count for the modifier.
        :type stack: int
        :param slot: Slot number for the modifier.
        :type slot: int
        :param sessionSlot: Session slot number for saving the data.
        :type sessionSlot: int
        """
        poke_id = existing_data['party'][slot]['id']
        modifier = {
            "args": [poke_id],
            "className": "NatureWeightModifier",
            "player": True,
            "stackCount": 10 if stack > 10 else stack,
            "typeId": "SOUL_DEW"
        }
        self.add_or_update_modifier(existing_data, modifier, "Soul Dew", slot, sessionSlot)

    def do_all_modifiers(self, existing_data, stack, slot, sessionSlot):
        """
        Adds or updates all modifiers at once.

        :param existing_data: Existing data to be modified.
        :type existing_data: dict
        :param stack: Stack count for the modifiers.
        :type stack: int
        :param slot: Slot number for the modifiers.
        :type slot: int
        :param sessionSlot: Session slot number for saving the data.
        :type sessionSlot: int
        """
        all_modifiers = [
            self.ABILITY_CHARM, self.SHINY_CHARM, self.EXP_CHARM, self.SUPER_EXP_CHARM,
            self.GOLDEN_EXP_CHARM, self.HEALING_CHARM, self.MINI_BLACK_HOLE, self.MULTI_LENS,
            self.REVIVER_SEED, self.LOCK_CAPSULE, self.GRIP_CLAW, self.GOLDEN_PUNCH, self.EXP_BALANCE,
            self.CANDY_JAR, self.AMULET_COIN, self.BERRY_POUCH, self.SHELL_BELL, self.SOUL_DEW
        ]
        for modifier_func in all_modifiers:
            modifier_func(existing_data, stack, slot, sessionSlot)

    def print_modifiers(self, existing_data):
        """
        Prints all current modifiers in the existing data.

        :param existing_data: Existing data containing modifiers.
        :type existing_data: dict
        """
        if 'modifiers' not in existing_data or not existing_data['modifiers']:
            print("No modifiers found.")
            return
        
        for modifier in existing_data['modifiers']:
            print(json.dumps(modifier, indent=4))
