import json
from utilities import cFormatter, Color

class ModifierEditor:
    def __init__(self, slot):
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
            (("Return to Menu", ''), self.end),
            ("pyRogue Item Editor", 'title'),
        ]

        self.slot = slot

    @staticmethod
    def end(self):
        return None

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
        """Ensure the 'modifiers' block is present and return stack count for given type_id."""
        if 'modifiers' not in data or not isinstance(data['modifiers'], list):
            data['modifiers'] = []

        # Look for existing modifier with matching type_id
        for modifier in data['modifiers']:
            if modifier.get('typeId') == type_id:
                return modifier.get('stackCount', 0)
        return None

    @staticmethod
    def add_or_update_modifier(data, modifier, modifier_name, slot):
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
        
        ModifierEditor.save_json(data, f'slot_{slot}.json')
        cFormatter.print(Color.GREEN, f'Successfully added {modifier["stackCount"]} {modifier_name}.')
        cFormatter.print(Color.INFO, 'Some items are limited, hence why it didn\'t apply all you may wanted.')

    def user_menu(self):
        try:
            while True:
                existing_data = ModifierEditor.load_json(f'slot_{self.slot}.json')
                valid_choices = cFormatter.initialize_menu(self.menu_items)
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
                                self.print_modifiers(existing_data)
                                break

                            slot = int(input('Select the Pokemon slot you want to edit (0-5): '))
                            if slot < 0 or slot > 5:
                                print('Invalid session slot.')
                                continue

                            if function_name == 'do_all_modifiers':
                                stack = int(input('How many all listed modifiers do you want?: '))
                                self.do_all_modifiers(existing_data, stack, slot)
                                break
                            
                            # Get stack count or prompt for new stack amount
                            stacks_raw = self.ensure_modifiers_block(existing_data, function_name)
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
                                
    def ABILITY_CHARM(self, existing_data, stack, slot):
        modifier = {
            "className": "HiddenAbilityRateBoosterModifier",
            "args": None,
            "player": True,
            "stackCount": 10 if stack > 10 else stack,
            "typeId": "ABILITY_CHARM"
        }
        self.add_or_update_modifier(existing_data, modifier, "Hidden Ability Rate Booster Modifier", slot)

    def SHINY_CHARM(self, existing_data, stack, slot):
        modifier = {
            "args": None,
            "className": "ShinyRateBoosterModifier",
            "player": True,
            "stackCount": 4 if stack > 4 else stack,
            "typeId": "SHINY_CHARM"
        }
        self.add_or_update_modifier(existing_data, modifier, "Shiny Rate Booster Modifier", slot)

    def EXP_CHARM(self, existing_data, stack, slot):
        modifier = {
            "args": [25],
            "className": "ExpBoosterModifier",
            "player": True,
            "stackCount": 99 if stack > 99 else stack,
            "typeId": "EXP_CHARM"
        }
        self.add_or_update_modifier(existing_data, modifier, "EXP Charm", slot)

    def SUPER_EXP_CHARM(self, existing_data, stack, slot):
        modifier = {
            "args": [60],
            "className": "ExpBoosterModifier",
            "player": True,
            "stackCount": 30 if stack > 30 else stack,
            "typeId": "SUPER_EXP_CHARM"
        }
        self.add_or_update_modifier(existing_data, modifier, "Super EXP Charm", slot)

    def GOLDEN_EXP_CHARM(self, existing_data, stack, slot):
        modifier = {
            "args": [100],
            "className": "ExpBoosterModifier",
            "player": True,
            "stackCount": 10 if stack > 10 else stack,
            "typeId": "GOLDEN_EXP_CHARM",
        }
        self.add_or_update_modifier(existing_data, modifier, "Golden EXP Charm", slot)

    def HEALING_CHARM(self, existing_data, stack, slot):
        modifier = {
            "args": [1.1],
            "className": "HealingBoosterModifier",
            "player": True,
            "stackCount": 5 if stack > 5 else stack,
            "typeId": "HEALING_CHARM",
        }
        self.add_or_update_modifier(existing_data, modifier, "Healing Booster Modifier", slot)

    def LOCK_CAPSULE(self, existing_data, stack, slot):
        modifier = {
            "args": None,
            "className": "LockModifierTiersModifier",
            "player": True,
            "stackCount": 1 if stack > 1 else stack,
            "typeId": "LOCK_CAPSULE",
        }
        self.add_or_update_modifier(existing_data, modifier, "Lock Modifier Tiers Modifier", slot)

    def EXP_BALANCE(self, existing_data, stack, slot):
        modifier = {
            "args": None,
            "className": "ExpBalanceModifier",
            "player": True,
            "stackCount": 4 if stack > 4 else stack,
            "typeId": "EXP_BALANCE"
        }
        self.add_or_update_modifier(existing_data, modifier, "EXP Balance Modifier", slot)

    def CANDY_JAR(self, existing_data, stack, slot):
        modifier = {
            "args": None,
            "className": "LevelIncrementBoosterModifier",
            "player": True,
            "stackCount": 99 if stack > 99 else stack,
            "typeId": "CANDY_JAR"
        }
        self.add_or_update_modifier(existing_data, modifier, "Level Increment Booster Modifier", slot)

    def AMULET_COIN(self, existing_data, stack, slot):
        modifier = {
            "args": None,
            "className": "MoneyMultiplierModifier",
            "player": True,
            "stackCount": 5 if stack > 5 else stack,
            "typeId": "AMULET_COIN"
        }
        self.add_or_update_modifier(existing_data, modifier, "Money Multiplier Modifier", slot)

    def BERRY_POUCH(self, existing_data, stack, slot):
        modifier = {
            "args": None,
            "className": "PreserveBerryModifier",
            "player": True,
            "stackCount": 3 if stack > 3 else stack,
            "typeId": "BERRY_POUCH"
        }
        self.add_or_update_modifier(existing_data, modifier, "Preserve Berry Modifier", slot)

    def SHELL_BELL(self, existing_data, stack, slot):
        poke_id = existing_data['party'][slot]['id']
        modifier = {
            "args": [poke_id],
            "className": "HitHealModifier",
            "player": True,
            "stackCount": 9 if stack > 9 else stack,
            "typeId": "SHELL_BELL",
        }
        self.add_or_update_modifier(existing_data, modifier, "Hit Heal Modifier", slot)

    def SOUL_DEW(self, existing_data, stack, slot):
        poke_id = existing_data['party'][slot]['id']
        modifier = {
            "args": [poke_id],
            "className": "PokemonNatureWeightModifier",
            "player": True,
            "stackCount": 10 if stack > 10 else stack,
            "typeId": "SOUL_DEW"
        }
        self.add_or_update_modifier(existing_data, modifier, "Pokemon Nature Weight Modifier", slot)


    def GRIP_CLAW(self, existing_data, stack, slot):
        poke_id = existing_data['party'][slot]['id']
        modifier = {
            "args": [poke_id, '10'],
            "className": "ContactHeldItemTransferChanceModifier",
            "player": True,
            "stackCount": 5 if stack > 5 else stack,
            "typeId": "GRIP_CLAW",
        }
        self.add_or_update_modifier(existing_data, modifier, "Contact Held Item Transfer Chance Modifier", slot)

    def GOLDEN_PUNCH(self, existing_data, stack, slot):
        poke_id = existing_data['party'][slot]['id']
        modifier = {
            "args": [poke_id],
            "className": "DamageMoneyRewardModifier",
            "player": True,
            "stackCount": 5 if stack > 5 else stack,
            "typeId": "GOLDEN_PUNCH",
        }
        self.add_or_update_modifier(existing_data, modifier, "Damage Money Reward Modifier", slot)

    def MINI_BLACK_HOLE(self, existing_data, stack, slot):
        poke_id = existing_data['party'][slot]['id']
        modifier = {
            "args": [poke_id],
            "className": "TurnHeldItemTransferModifier",
            "player": True,
            "stackCount": 1 if stack > 1 else stack,
            "typeId": "MINI_BLACK_HOLE",
        }
        self.add_or_update_modifier(existing_data, modifier, "Turn Held Item Transfer Modifier", slot)

    def MULTI_LENS(self, existing_data, stack, slot):
        poke_id = existing_data['party'][slot]['id']
        modifier = {
            "args": [poke_id],
            "className": "PokemonMultiHitModifier",
            "player": True,
            "stackCount": 3 if stack > 3 else stack,
            "typeId": "MULTI_LENS",
        }
        self.add_or_update_modifier(existing_data, modifier, "Pokemon Multi-Hit Modifier", slot)

    def REVIVER_SEED(self, existing_data, stack, slot):
        poke_id = existing_data['party'][slot]['id']
        modifier = {
            "args": [poke_id],
            "className": "PokemonInstantReviveModifier",
            "player": True,
            "stackCount": 1 if stack > 1 else stack,
            "typeId": "REVIVER_SEED",
        }
        self.add_or_update_modifier(existing_data, modifier, "Pokemon Instant Revive Modifier", slot)

    def do_all_modifiers(self, existing_data, stack, slot):
        all_modifiers = [
            self.ABILITY_CHARM, self.SHINY_CHARM, self.EXP_CHARM, self.SUPER_EXP_CHARM,
            self.GOLDEN_EXP_CHARM, self.HEALING_CHARM, self.MINI_BLACK_HOLE, self.MULTI_LENS,
            self.REVIVER_SEED, self.LOCK_CAPSULE, self.GRIP_CLAW, self.GOLDEN_PUNCH, self.EXP_BALANCE,
            self.CANDY_JAR, self.AMULET_COIN, self.BERRY_POUCH, self.SHELL_BELL, self.SOUL_DEW
        ]
        for modifier_func in all_modifiers:
            modifier_func(existing_data, stack, slot)

    def print_modifiers(self, existing_data):
        if 'modifiers' not in existing_data or not existing_data['modifiers']:
            print("No modifiers found.")
            return
        
        for modifier in existing_data['modifiers']:
            print(json.dumps(modifier, indent=4))

if __name__ == '__main__':
    editor = ModifierEditor()
    editor.user_menu()
