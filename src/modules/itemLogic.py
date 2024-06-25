# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/JulianStiebler/
# Date of release: 23.06.2024 
# Last Edited: 25.06.2024
# Based on: https://github.com/pagefaultgames/pokerogue/

# Unlike the other code, reusing this in your own project is forbidden.

import json
from utilities import cFormatter, Color
from colorama import Fore, Style
from enum import Enum
from dataclasses import dataclass, field
from typing import Any, List, Optional
from modules.config import version
from collections import defaultdict


@dataclass
class Modifier:
    args: Optional[List[Any]]
    className: str
    player: bool
    stackCount: int
    typeId: str
    typePregenArgs: Optional[List[Any]] = None
    description: Optional[str] = field(default=None, repr=False, compare=False)
    customName: Optional[str] = field(default=None, repr=False, compare=False)
    customType: Optional[str] = field(default=None, repr=False, compare=False)
    maxStack: Optional[int] = field(default=None, repr=False, compare=False)
    shortDescription: Optional[str] = field(default=None, repr=False, compare=False)

    def to_json(self, poke_id: Optional[int] = None) -> dict:
        original_args = self.args  # Store original args for potential reset later

        # Replace None with poke_id in args if necessary
        if self.args is not None:
            self.args = [poke_id if arg is None else arg for arg in self.args]

        # Create JSON representation
        json_data = {
            "args": self.args if self.args else None,  # Ensures args is None if empty
            "className": self.className,
            "player": self.player,
            "stackCount": self.stackCount,
            "typeId": self.typeId,
        }
        if self.typePregenArgs is not None:
            json_data["typePregenArgs"] = self.typePregenArgs

        # Reset args to original state after using modified version
        self.args = original_args

        return json_data

# customName needs to be localized later
class ModifierType(Enum):
    #Stat boosting Items
    SILK_SCARF = Modifier(args=[None, 0, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[0], description='Boosts NORMAL types.', customName='Silk Scarf', customType='StatBooster', maxStack='99')                           
    BLACK_BELT = Modifier(args=[None, 1, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[1], description='Boosts FIGHT types.', customName='Black Belt', customType='StatBooster', maxStack='99', shortDescription='Test')
    SHARP_BEAK = Modifier(args=[None, 2, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[2], description='Boosts FLYING types.', customName='Sharp Beak', customType='StatBooster', maxStack='99')
    POISON_BARB = Modifier(args=[None, 3, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[3], description='Boosts POISON types.', customName='Poison Barb', customType='StatBooster', maxStack='99')
    SOFT_SAND = Modifier(args=[None, 4, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[4], description='Boosts GROUND types.', customName='Soft Sand', customType='StatBooster', maxStack='99')
    HARD_STONE = Modifier(args=[None, 5, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[5], description='Boosts ROCK types.', customName='Hard Stone', customType='StatBooster', maxStack='99')
    SILVER_POWDER = Modifier(args=[None, 6, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[6], description='Boosts BUG types.', customName='Silver Powder', customType='StatBooster', maxStack='99')
    SPELL_TAG = Modifier(args=[None, 7, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[7], description='Boosts GHOST types.', customName='Spell Tag', customType='StatBooster', maxStack='99')
    METAL_COAT = Modifier(args=[None, 8, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[8], description='Boosts STEEL types.', customName='Metal Coat', customType='StatBooster', maxStack='99')
    CHARCOAL = Modifier(args=[None, 9, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[9], description='Boosts FIRE types.', customName='Charcoal', customType='StatBooster', maxStack='99')
    MYSTIC_WATER = Modifier(args=[None, 10, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[10], description='Boosts WATER types.', customName='Mystic Water', customType='StatBooster', maxStack='99')
    MIRACLE_SEED = Modifier(args=[None, 11, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[11], description='Boosts GRASS types.', customName='Miracle Seed', customType='StatBooster', maxStack='99')
    MAGNET = Modifier(args=[None, 12, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[12], description='Boosts ELECTRIC types.', customName='Magnet', customType='StatBooster', maxStack='99')
    TWISTED_SPOON = Modifier(args=[None, 13, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[13], description='Boosts PSYCHO types.', customName='Twisted Spoon', customType='StatBooster', maxStack='99')
    NEVER_MELT_ICE = Modifier(args=[None, 14, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[14], description='Boosts ICE types.', customName='Never Melt Ice', customType='StatBooster', maxStack='99')
    DRAGON_FANG = Modifier(args=[None, 15, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[15], description='Boosts DRAGON types.', customName='Dragon Fang', customType='StatBooster', maxStack='99')
    BLACK_GLASSES = Modifier(args=[None, 16, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[16], description='Boosts DARK types.', customName='Black Glasses', customType='StatBooster', maxStack='99')
    FAIRY_FEATHER = Modifier(args=[None, 17, 20], className='AttackTypeBoosterModifier', player=True, stackCount=1, typeId='ATTACK_TYPE_BOOSTER', typePregenArgs=[17], description='Boosts FAIRY types.', customName='Fairy Feather', customType='StatBooster', maxStack='99')
    # Vitamins
    HP_UP = Modifier(args=[None, 0], className='PokemonBaseStatModifier', player=True, stackCount=1, typeId='BASE_STAT_BOOSTER', typePregenArgs=[0], description='Increases HP.', customName='HP Up', customType='Vitamin', maxStack='20')
    PROTEIN = Modifier(args=[None, 1], className='PokemonBaseStatModifier', player=True, stackCount=1, typeId='BASE_STAT_BOOSTER', typePregenArgs=[1], description='Increases Attack.', customName='Protein', customType='Vitamin', maxStack='20')
    IRON = Modifier(args=[None, 2], className='PokemonBaseStatModifier', player=True, stackCount=1, typeId='BASE_STAT_BOOSTER', typePregenArgs=[2], description='Increases Defense.', customName='Iron', customType='Vitamin', maxStack='20')
    CALCIUM = Modifier(args=[None, 3], className='PokemonBaseStatModifier', player=True, stackCount=1, typeId='BASE_STAT_BOOSTER', typePregenArgs=[3], description='Increases Special Attack.', customName='Calcium', customType='Vitamin', maxStack='20')
    ZINC = Modifier(args=[None, 4], className='PokemonBaseStatModifier', player=True, stackCount=1, typeId='BASE_STAT_BOOSTER', typePregenArgs=[4], description='Increases Special Defense.', customName='Zinc', customType='Vitamin', maxStack='20')
    CARBOS = Modifier(args=[None, 5], className='PokemonBaseStatModifier', player=True, stackCount=1, typeId='BASE_STAT_BOOSTER', typePregenArgs=[5], description='Increases Speed.', customName='Carbos', customType='Vitamin', maxStack='20')
    #X Attack
    X_ATTACK = Modifier(args=[0, 5], className='TempBattleStatBoosterModifier', player=True, stackCount=1, typeId='TEMP_STAT_BOOSTER', typePregenArgs=[0], description='Increases Attack', customName='X Attack', customType='XItem', maxStack='99')
    X_DEFENSE = Modifier(args=[1, 5], className='TempBattleStatBoosterModifier', player=True, stackCount=1, typeId='TEMP_STAT_BOOSTER', typePregenArgs=[1], description='Increases Defense', customName='X Defense', customType='XItem', maxStack='99')
    X_SP_ATK = Modifier(args=[2, 5], className='TempBattleStatBoosterModifier', player=True, stackCount=1, typeId='TEMP_STAT_BOOSTER', typePregenArgs=[2], description='Increases Special Attack', customName='X Special Attack', customType='XItem', maxStack='99')
    X_SP_DEF = Modifier(args=[3, 5], className='TempBattleStatBoosterModifier', player=True, stackCount=1, typeId='TEMP_STAT_BOOSTER', typePregenArgs=[3], description='Increases Special Defense', customName='X Special Defense', customType='XItem', maxStack='99')
    X_SPEED = Modifier(args=[4, 5], className='TempBattleStatBoosterModifier', player=True, stackCount=1, typeId='TEMP_STAT_BOOSTER', typePregenArgs=[4], description='Increases Speed', customName='X Speed', customType='XItem', maxStack='99')
    X_ACCURACY = Modifier(args=[5, 5], className='TempBattleStatBoosterModifier', player=True, stackCount=1, typeId='TEMP_STAT_BOOSTER', typePregenArgs=[5], description='Increases Accuracy', customName='X Accuracy', customType='XItem', maxStack='99')
    X_DIRE_HIT = Modifier(args=[6, 5], className='TempBattleStatBoosterModifier', player=True, stackCount=1, typeId='TEMP_STAT_BOOSTER', typePregenArgs=[6], description='Increases Critical%', customName='X Dire Hit', customType='XItem', maxStack='99')
    # Berrys
    APICOT_BERRY = Modifier(args=[None, 6], className='BerryModifier', player=True, stackCount=1, typeId='BERRY', typePregenArgs=[6], shortDescription='+SP Def when below 25% HP', description='Raises Sp. Def if HP is below 25%.', customName='Apicot Berry', customType='Berry', maxStack='3')
    ENIGMA_BERRY = Modifier(args=[None, 2], className='BerryModifier', player=True, stackCount=1, typeId='BERRY', typePregenArgs=[2], shortDescription='Heals 25% when critical hit', description='Restores 25% HP if hit by a super effective move.', customName='Enigma Berry', customType='Berry', maxStack='2')
    GANLON_BERRY = Modifier(args=[None, 4], className='BerryModifier', player=True, stackCount=1, typeId='BERRY', typePregenArgs=[4], shortDescription='Raise Defense when below 25% HP',description='Raises Defense if HP is below 25%.', customName='Ganlon Berry', customType='Berry', maxStack='3')
    LANSAT_BERRY = Modifier(args=[None, 8], className='BerryModifier', player=True, stackCount=1, typeId='BERRY', typePregenArgs=[8], shortDescription='Raise Crit when below 25% HP', description='Raises critical hit ratio if HP is below 25%.', customName='Lansat Berry', customType='Berry', maxStack='3')
    LIECHI_BERRY = Modifier(args=[None, 3], className='BerryModifier', player=True, stackCount=1, typeId='BERRY', typePregenArgs=[3], shortDescription='Raise ATK when below 25% HP', description='Raises Attack if HP is below 25%.', customName='Liechi Berry', customType='Berry', maxStack='3')
    LEPPA_BERRY = Modifier(args=[None, 10], className='BerryModifier', player=True, stackCount=1, typeId='BERRY', typePregenArgs=[10], shortDescription='Restore 10 PP when empty', description='Restores 10 PP to a move if its PP reaches 0.', customName='Leppa Berry', customType='Berry', maxStack='2')
    LUM_BERRY = Modifier(args=[None, 1], className='BerryModifier', player=True, stackCount=1, typeId='BERRY', typePregenArgs=[1], shortDescription='Cures non-volatiles status', description='Cures any non-volatile status condition and confusion', customName='Lum Berry', customType='Berry', maxStack='2') 
    PETAYA_BERRY = Modifier(args=[None, 5], className='BerryModifier', player=True, stackCount=1, typeId='BERRY', typePregenArgs=[5], description='Raises Sp. Atk if HP is below 25%.', customName='Petaya Berry', customType='Berry', maxStack='3')
    SALAC_BERRY = Modifier(args=[None, 7], className='BerryModifier', player=True, stackCount=1, typeId='BERRY', typePregenArgs=[7], description='Raises Speed if HP is below 25%.', customName='Salac Berry', customType='Berry', maxStack='3')
    SITRUS_BERRY = Modifier(args=[None, 0], className='BerryModifier', player=True, stackCount=1, typeId='BERRY', typePregenArgs=[0], description='Restores 25% HP if HP is below 50%.', customName='Sitrus Berry', customType='Berry', maxStack='2') 
    STARF_BERRY = Modifier(args=[None, 9], className='BerryModifier', player=True, stackCount=1, typeId='BERRY', typePregenArgs=[9], description='+Random stat if HP is below 25%.', customName='Starf Berry', customType='Berry', maxStack='3')
    BERRY_POUCH = Modifier(args=None, className='PreserveBerryModifier', player=True, stackCount=1, typeId='BERRY_POUCH', description='33% chance used berry to not be used.', customName='Berry Pouch', customType='Berry', maxStack='3')
    # Passive Boosts
    GOLDEN_POKEBALL = Modifier(args=None, className='ExtraModifierModifier', player=True, stackCount=1, typeId='GOLDEN_POKEBALL', shortDescription='One more shop item', description='Adds 1 extra item option at the end of every battle.', customName='Golden Pokeball', customType='PassiveBoost', maxStack='3')
    AMULET_COIN = Modifier(args=None, className='MoneyMultiplierModifier', player=True, stackCount=1, typeId='AMULET_COIN', shortDescription='+20% Money from all sources', description='Increases money rewards from all sources by 20%.', customName='Amulet Coin', customType='PassiveBoost', maxStack='5')                                                                 
    LOCK_CAPSULE = Modifier(args=None, className='LockModifierTiersModifier', player=True, stackCount=1, typeId='LOCK_CAPSULE', shortDescription='Lock rarity in shops', description='Allows you to lock item rarities when rerolling items.', customName='Lock Capsule', customType='PassiveBoost', maxStack='1')
    CANDY_JAR = Modifier(args=None, className='LevelIncrementBoosterModifier', player=True, stackCount=1, typeId='CANDY_JAR', shortDescription='+1 level per rare candy', description='Increases the number of levels added by Rare Candy items by 1.', customName='Candy Jar', customType='PassiveBoost', maxStack='99')
    EXP_SHARE = Modifier(args=None, className='ExpShareModifier', player=True, stackCount=1, typeId='EXP_SHARE', shortDescription='Share +20% XP with all', description='Non-participants receive 20% of a single participant\'s EXP. Points.', customName='EXP Share', customType='PassiveBoost', maxStack='5')
    EXP_BALANCE = Modifier(args=None, className='ExpBalanceModifier', player=True, stackCount=1, typeId='EXP_BALANCE', shortDescription='Weakest mon gets more XP', description='Balances 20% of your total earned exp towards the lowest leveled party member(s).', customName='EXP Balance', customType='PassiveBoost', maxStack='4')
    EXP_CHARM = Modifier(args=[25], className='ExpBoosterModifier', player=True, stackCount=1, typeId='EXP_CHARM', shortDescription='+25% EXP Gain', description='Increases gain of EXP. Points by 25%.', customName='EXP Charm', customType='PassiveBoost', maxStack='99')
    SUPER_EXP_CHARM = Modifier(args=[60], className='ExpBoosterModifier', player=True, stackCount=1, typeId='SUPER_EXP_CHARM', shortDescription='+60% EXP Gain', description='Increases gain of EXP. Points by 60%. ', customName='Super EXP Charm', customType='PassiveBoost', maxStack='30')
    GOLDEN_EXP_CHARM = Modifier(args=[100], className='ExpBoosterModifier', player=True, stackCount=1, typeId='GOLDEN_EXP_CHARM', shortDescription='+100% EXP Gain', description='Increases gain of EXP. Points by 100%. ', customName='Golden EXP Charm', customType='PassiveBoost', maxStack='10')
    SHINY_CHARM = Modifier(args=None, className='ShinyRateBoosterModifier', player=True, stackCount=1, typeId='SHINY_CHARM', shortDescription='Increase shiny encounter %', description='Dramatically increases the chance of a wild Pokémon being Shiny.', customName='Shiny Charm', customType='PassiveBoost', maxStack='4')
    ABILITY_CHARM = Modifier(args=None, className='HiddenAbilityRateBoosterModifier', player=True, stackCount=1, typeId='ABILITY_CHARM', shortDescription='Wild pokemon hidden ability chance increased', description='Dramatically increases the chance of a wild Pokémon having a Hidden Ability.', customName='Ability Charm', customType='PassiveBoost', maxStack='3')                                                    
    IV_SCANNER = Modifier(args=None, className='IvScannerModifier', player=True, stackCount=1, typeId='IV_SCANNER', shortDescription='Scan enemy IVs', description='Allows scanning the IVs of wild Pokémon. 2 IVs are revealed per stack. The best IVs are shown first.', customName='IV Scanner', customType='Danger', maxStack='1')
    MEGA_BRACELET = Modifier(args=None, className='MegaEvolutionAccessModifier', player=True, stackCount=1, typeId='MEGA_BRACELET', description='Mega Stones become available.', customName='Mega Bracelet', customType='PassiveBoost', maxStack='1')
    DYNAMAX_BAND = Modifier(args=None, className='GigantamaxAccessModifier', player=True, stackCount=1, typeId='DYNAMAX_BAND', description='Max Mushrooms become available.', customName='Dynamax Band', customType='PassiveBoost', maxStack='1')
    TERA_ORB = Modifier(args=None, className='TerastallizeAccessModifier', player=True, stackCount=1, typeId='TERA_ORB', description='Tera Shards become available.', customName='Tera Orb', customType='PassiveBoost', maxStack='3')
    HEALING_CHARM = Modifier(args=[1.1], className='HealingBoosterModifier', player=True, stackCount=1, typeId='HEALING_CHARM', shortDescription='HP restoring moves heal 10% more', description='Increases the effectiveness of HP restoring moves and items by 10% (excludes Revives).', customName='Healing Charm', customType='PassiveBoost', maxStack='5')
    # Other holdables
    REVIVER_SEED = Modifier(args=[None], className='PokemonInstantReviveModifier', player=True, stackCount=1, typeId='REVIVER_SEED', description='Revives the holder for 1/2 HP upon fainting.', customName='Reviver Seed', customType='OtherHoldable', maxStack='1')
    GOLDEN_PUNCH = Modifier(args=[None], className='DamageMoneyRewardModifier', player=True, stackCount=1, typeId='GOLDEN_PUNCH', description='Grants 50% of damage inflicted as money.', customName='Golden Punch', customType='OtherHoldable', maxStack='5')
    WIDE_LENS = Modifier(args=[None, 5], className='PokemonMoveAccuracyBoosterModifier', player=True, stackCount=1, typeId='WIDE_LENS', description='Increases move accuracy by 5 (maximum 100).', customName='Wide Lens', customType='OtherHoldable', maxStack='3')
    BATON = Modifier(args=[None], className='SwitchEffectTransferModifier', player=True, stackCount=1, typeId='BATON', shortDescription='Pass on effects when switching Pokemon', description='Allows passing along effects when switching Pokémon, which also bypasses traps.', customName='Baton', customType='OtherHoldable', maxStack='1')
    FOCUS_BAND = Modifier(args=[None], className='SurviveDamageModifier', player=True, stackCount=1, typeId='FOCUS_BAND', description='10% chance to cheat death with 1HP', customName='Focus Band', customType='OtherHoldable', maxStack='4')
    GRIP_CLAW = Modifier(args=[None, 10], className='ContactHeldItemTransferChanceModifier', player=True, stackCount=1, typeId='GRIP_CLAW', shortDescription='10% onhit to steal enemy item', description='Upon attacking, there is a 10% chance the foe\'s held item will be stolen.', customName='Grip Claw', customType='OtherHoldable', maxStack='5')
    QUICK_CLAW = Modifier(args=[None], className='BypassSpeedChanceModifier', player=True, stackCount=1, typeId='QUICK_CLAW', shortDescription='10% chance to go first ignoring speed', description='Adds a 10percent chance to move first regardless of speed (after priority)', customName='Quick Claw', customType='OtherHoldable', maxStack='3')
    KINGS_ROCK = Modifier(args=[None], className='FlinchChanceModifier', player=True, stackCount=1, typeId='KINGS_ROCK', shortDescription='10% onhit to make enemy flinch', description='Adds a 10% chance an attack move will cause the opponent to flinch.', customName='Kings Rock', customType='OtherHoldable', maxStack='3')
    LEFTOVERS = Modifier(args=[None], className='TurnHealModifier', player=True, stackCount=1, typeId='LEFTOVERS', description='Heals 1/16 of a Pokémon\'s maximum HP every turn.', customName='Leftovers', customType='OtherHoldable', maxStack='4')
    SHELL_BELL = Modifier(args=[None], className='HitHealModifier', player=True, stackCount=1, typeId='SHELL_BELL', description='Heals 1/8 of the Pokemon\'s dealt damage.', customName='Shell Bell', customType='OtherHoldable', maxStack='4')
    SOOTHE_BELL = Modifier(args=[None], className='PokemonFriendshipBoosterModifier', player=True, stackCount=1, typeId='SOOTHE_BELL', shortDescription='+50% more friendship per win', description='Increases friendship gain per victory by 50%.', customName='Soothe Bell', customType='OtherHoldable', maxStack='3')
    SOUL_DEW = Modifier(args=[None], className='PokemonNatureWeightModifier', player=True, stackCount=1, typeId='SOUL_DEW', shortDescription='Increase nature influence (additive +10%)', description='Increases the influence of a Pokémon\'s nature on its stats by 10% (additive).', customName='Soul Dew', customType='OtherHoldable', maxStack='10')
    MULTI_LENS = Modifier(args=[None], className='PokemonMultiHitModifier', player=True, stackCount=1, typeId='MULTI_LENS', shortDescription='Attacks hit one additional time', description='Attacks hit one additional time at the cost of a 60/75/82.5% power reduction per stack respectively.', customName='Multi Lens', customType='OtherHoldable', maxStack='3')
    MINI_BLACK_HOLE = Modifier(args=[None], className='TurnHeldItemTransferModifier', player=True, stackCount=1, typeId='MINI_BLACK_HOLE', shortDescription='Steal one item each turn from enemy', description='Every turn, the holder acquires one held item from the foe.', customName='Mini Black Hole', customType='OtherHoldable', maxStack='1')
    LUCKY_EGG = Modifier(args=[None, 40], className='PokemonExpBoosterModifier', player=True, stackCount=1, typeId='LUCKY_EGG', shortDescription='+40% EXP Gain', description='Increases the holder\'s gain of EXP. Points by 40%.', customName='Lucky Egg', customType='OtherHoldable', maxStack='99')
    GOLDEN_EGG = Modifier(args=[None, 100], className='PokemonExpBoosterModifier', player=True, stackCount=1, typeId='GOLDEN_EGG', shortDescription='+100% EXP Gain', description='Increases the holder\'s gain of EXP. Points by 100%. ', customName='Golden Pokbeall', customType='OtherHoldable', maxStack='99')
    #FORM_CHANGE_ITEM0 = Modifier(args=[None, 0, True], className='PokemonFormChangeItemModifier', player=True, stackCount=1, typeId='FORM_CHANGE_ITEM', typePregenArgs=[0], description='Causes certain Pokémon to change form.', customName='FormChangeItem', customType='OtherHoldable', maxStack='1')
    # the form change exists from 0-70... 
    # Dangerous Items
    TOXIC_ORB = Modifier(args=[None], className='TurnStatusEffectModifier', player=True, stackCount=1, typeId='TOXIC_ORB', shortDescription='Poison your pokemon', description='Badly poisons its holder at the end of the turn if they do not have a status condition already', customName='Toxic Orb', customType='Danger', maxStack='1')
    FIRE_ORB = Modifier(args=[None], className='TurnStatusEffectModifier', player=True, stackCount=1, typeId='FIRE_ORB', shortDescription='Burn your pokemon', description='Burns its holder at the end of the turn if they do not have a status condition already.', customName='Fire Orb', customType='Danger', maxStack='1')

    

class ModifierEditor:
    def __init__(self):
        self.menu_items = self.create_menu_items()
        self.notify_message = None

    def create_menu_items(self):
        menu_items = [(f'{version}', 'title')]

        # Group the modifiers by customType
        modifiers_by_type = defaultdict(list)
        for modifier in ModifierType:
            modifiers_by_type[modifier.value.customType].append(modifier)

        # Define the order of categories
        category_order = [
            'StatBooster',
            'Vitamin',
            'XItem',
            'Berry',
            'PassiveBoost',
            'OtherHoldable',
            'Danger'  # Assuming Orb as 'Danger' type based on your examples
        ]

        # Dynamically create menu items based on the customType categories
        for category in category_order:
            if category in modifiers_by_type:
                if category == 'Danger':
                    menu_items.append(('Not included in Give All', 'category'))
                else:
                    menu_items.append((category, 'category'))
                menu_items.extend(self.create_menu_items_chunk(modifiers_by_type[category]))

        # Add closing part
        menu_items.append(('pyRogue Item Editor', 'category'))
        menu_items.append((('Give all Modifiers', "Give All"), self.do_all_modifiers))
        menu_items.append((('Return to Main Menu', f'{Fore.LIGHTYELLOW_EX}Use when done'), self.end))
        menu_items.append(('You can also STRG+C to return to the Main Menu', 'category'))
        menu_items.append(('You can save these changes in the Main Menu', 'category'))
        menu_items.append(('Enter any command to see what it does', 'category'))
        
        return menu_items

    def create_menu_items_chunk(self, modifiers):
        chunk = []
        for mod_type in modifiers:
            # Extracting the ModifierType name
            modifier = mod_type.value
            mod_description = modifier.shortDescription if modifier.shortDescription else modifier.description
            """
                # Combining typeId with typePregenArgs if present
                type_info = modifier.typeId
                if hasattr(modifier, 'typePregenArgs') and modifier.typePregenArgs:
                    type_info += f" ({', '.join(map(str, modifier.typePregenArgs))})"
                # Appending to chunk
            """
            chunk.append(((modifier.customName, f'{mod_description} - (Max. {modifier.maxStack})'), mod_type))
        return chunk

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
    def ensure_modifiers_block(data, type_id, type_pregen_args, poke_id):
        if 'modifiers' not in data or not isinstance(data['modifiers'], list):
            data['modifiers'] = []
        for modifier in data['modifiers']:
            if (modifier.get('typeId') == type_id and 
                modifier.get('typePregenArgs') == type_pregen_args and
                modifier.get('args') and modifier['args'][0] == poke_id):
                return modifier.get('stackCount', 0)
        return None


    def add_or_update_modifier(self, data, modifier_type: ModifierType, stack, poke_id, sessionSlot):
        try:
            modifier = modifier_type.value
            maxStack = int(modifier.maxStack)
            if stack > maxStack:
                stack = maxStack
                
            modifier.stackCount = stack

            # Save original args state
            original_args = modifier.args[:] if modifier.args else None

            # Handle args with poke_id
            if modifier.args:
                modifier.args = [poke_id if arg is None else arg for arg in modifier.args]
                # print(f"Original modifier.args: {original_args}, Modified modifier.args with poke_id: {modifier.args}")

            if 'modifiers' not in data or not isinstance(data['modifiers'], list):
                data['modifiers'] = []

            def modifiers_match(existing_modifier, new_modifier):
                if existing_modifier['typeId'] != new_modifier['typeId']:
                    return False
                if existing_modifier.get('args') != new_modifier.get('args'):
                    return False
                if existing_modifier.get('typePregenArgs') != new_modifier.get('typePregenArgs'):
                    return False
                return True

            existing = next(
                (m for m in data['modifiers'] if modifiers_match(m, modifier.to_json(poke_id))),
                None
            )

            if existing:
                # print(f'Existing modifier JSON: {existing}')
                if existing['stackCount'] != modifier.stackCount:
                    existing['stackCount'] = modifier.stackCount
                    message = f'Successfully updated {modifier.stackCount} {modifier.typeId} to slot_{sessionSlot} for Pokémon ID {poke_id}' if modifier.args else f'Successfully updated {modifier.stackCount} {modifier.typeId} to slot_{sessionSlot}'
                else:
                    message = f'No change for {modifier.typeId} in slot_{sessionSlot} for Pokémon ID {poke_id}' if modifier.args else f'No change for {modifier.typeId} in slot_{sessionSlot}'
            else:
                data['modifiers'].append(modifier.to_json(poke_id))
                message = f'Successfully written {modifier.stackCount} {modifier.typeId} to slot_{sessionSlot} for Pokémon ID {poke_id}' if modifier.args else f'Successfully written {modifier.stackCount} {modifier.typeId} to slot_{sessionSlot}'

            # Restore original args state
            modifier.args = original_args

            self.save_json(data, f'slot_{sessionSlot}.json')
            cFormatter.print(Color.GREEN, message)
            self.notify_message = (f'Successfully added or updated modifier {modifier.typeId}', 'success')

        except Exception as e:
            self.notify_message = (f'Something went wrong. \n {e}', 'error')
            cFormatter.print(Color.INFO, f'Something went wrong. \n {e}', 'error')


    def user_menu(self, sessionSlot):
        existing_data = self.load_json(f'slot_{sessionSlot}.json')
        while True:
            if existing_data['gameMode'] == 3:
                break
            try:
                print('')
                valid_choices = cFormatter.m_initializeMenu(self.menu_items, length=75)
                if self.notify_message:
                    if self.notify_message[1] == 'success':
                        cFormatter.print(Color.GREEN, f'{self.notify_message[0]}')
                    elif self.notify_message[1] == 'error':
                        cFormatter.print(Color.CRITICAL, f'{self.notify_message[0]}', isLogging=True)
                    elif self.notify_message[1] == 'warning':
                        cFormatter.print(Color.WARNING, f'{self.notify_message[0]}')

                choice = int(input('Select an option by number: ').strip())
                selected_item = next((item for item in valid_choices if item[0] == choice), None)

                if selected_item is None:
                    cFormatter.print(Color.ERROR, 'Invalid choice, please try again.')
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
                    cFormatter.print(Color.DEBUG, 'You can always go back to the menu by typing anything not 0-5.')
                    cFormatter.print(Color.DEBUG, f'Item Description: {Style.RESET_ALL}{selected_modifier.value.description}')
                    cFormatter.print(Color.DEBUG, f'Max Stacks: {Style.RESET_ALL}{selected_modifier.value.maxStack}')
                    
                    party_num_input = input('Select the party slot of the Pokémon you want to edit (0-5): ')
                    try:
                        party_num = int(party_num_input)
                        if party_num < 0 or party_num > 5:
                            raise ValueError
                    except ValueError:
                        cFormatter.print(Color.DEBUG, 'Returning to the menu...')
                        continue
                    
                    poke_id = existing_data['party'][party_num]['id']
                    
                    stacks_raw = self.ensure_modifiers_block(existing_data, selected_modifier.value.typeId, selected_modifier.value.typePregenArgs, poke_id)
                    
                    while True:
                        if stacks_raw is not None:
                            stack_count_input = input(f'You already have {stacks_raw} of {selected_modifier.value.customName}. Set new value to: ')
                        else:
                            stack_count_input = input(f'How many {selected_modifier.value.customName} do you want? or enter any invalid input to retry: ')
                        try:
                            stack_count = int(stack_count_input)
                            break
                        except ValueError:
                            cFormatter.print(Color.ERROR, 'Invalid input. Please enter a valid number.')

                    self.add_or_update_modifier(existing_data, selected_modifier, stack_count, poke_id, sessionSlot)

            except ValueError:
                cFormatter.print(Color.ERROR, "Invalid input, please enter a number.")
            except KeyboardInterrupt:
                return

    def do_all_modifiers(self, sessionSlot):
        try:
            party_num = int(input('Select the party slot of the Pokémon you want to edit (0-5): '))
            if party_num < 0 or party_num > 5:
                message = 'Invalid party slot, please try again.'
                cFormatter.print(Color.ERROR, message)
                self.notify_message = (message, 'error')
                return

            stack_count = int(input('Enter the stack count for the modifiers: '))
            existing_data = self.load_json(f'slot_{sessionSlot}.json')
            poke_id = existing_data['party'][party_num]['id']
            try:
                for mod_type in ModifierType:
                    if mod_type.value.customType == 'Danger':
                        continue  # Skip modifiers with customType 'Danger'
                    self.add_or_update_modifier(existing_data, mod_type, stack_count, poke_id, sessionSlot)
            except Exception as e:
                self.notify_message = f'Something unexpected happened. {e}'
                cFormatter.print(Color.WARNING, f'Something unexpected happened. {e}', isLogging=True)
            finally:
                self.notify_message = ('Successfully added all modifiers except annoying ones.', 'success')
        except ValueError:
            cFormatter.print(Color.ERROR, 'Invalid input, please enter a number.')

    @staticmethod
    def end():
        cFormatter.print(Color.GREEN, 'Leaving pyRogue Item Editor.')

    @staticmethod
    def print_modifiers(sessionSlot):
        data = ModifierEditor.load_json(f'slot_{sessionSlot}.json')
        if 'modifiers' in data and isinstance(data['modifiers'], list):
            cFormatter.print(Color.INFO, 'Current Modifiers:')
            for modifier in data['modifiers']:
                cFormatter.print(Color.INFO, json.dumps(modifier, indent=4))
        else:
            cFormatter.print(Color.INFO, 'No modifiers found.')