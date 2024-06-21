import json
from utilities import cFormatter, Color
from colorama import Fore, Style
from typing import List, Any, Optional
from dataclasses import dataclass
from enum import Enum


@dataclass
class Modifier:
    display_name: str
    type_id: str
    class_name: str
    player: bool
    stack_count: int
    args: Optional[List[Any]] = None
    type_pregen_args: Optional[List[Any]] = None
    requires_pokemon_id: bool = False
    requires_chance: bool = False


class ModifierType(Enum):
    ABILITY_CHARM = Modifier(
        display_name="Hidden Ability Rate Booster Modifier",
        type_id="ABILITY_CHARM",
        class_name="HiddenAbilityRateBoosterModifier",
        player=True,
        stack_count=0
    )
    SHINY_CHARM = Modifier(
        display_name="Shiny Rate Booster Modifier",
        type_id="SHINY_CHARM",
        class_name="ShinyRateBoosterModifier",
        player=True,
        stack_count=0
    )
    EXP_CHARM = Modifier(
        display_name="EXP Charm",
        type_id="EXP_CHARM",
        class_name="ExpBoosterModifier",
        player=True,
        stack_count=0,
        args=[25]
    )
    SUPER_EXP_CHARM = Modifier(
        display_name="Super EXP Charm",
        type_id="SUPER_EXP_CHARM",
        class_name="ExpBoosterModifier",
        player=True,
        stack_count=0,
        args=[60]
    )
    GOLDEN_EXP_CHARM = Modifier(
        display_name="Golden EXP Charm",
        type_id="GOLDEN_EXP_CHARM",
        class_name="ExpBoosterModifier",
        player=True,
        stack_count=0,
        args=[100]
    )
    HEALING_CHARM = Modifier(
        display_name="Healing Booster Modifier",
        type_id="HEALING_CHARM",
        class_name="HealingBoosterModifier",
        player=True,
        stack_count=0,
        args=[1.1]
    )
    MINI_BLACK_HOLE = Modifier(
        display_name="On-hit item stealer",
        type_id="MINI_BLACK_HOLE",
        class_name="TurnHeldItemTransferModifier",
        player=True,
        stack_count=0,
        requires_pokemon_id=True
    )
    MULTI_LENS = Modifier(
        display_name="Multi-Hit Modifier",
        type_id="MULTI_LENS",
        class_name="PokemonMultiHitModifier",
        player=True,
        stack_count=0,
        requires_pokemon_id=True
    )
    REVIVER_SEED = Modifier(
        display_name="On-death revive",
        type_id="REVIVER_SEED",
        class_name="PokemonInstantReviveModifier",
        player=True,
        stack_count=0,
        requires_pokemon_id=True
    )
    LOCK_CAPSULE = Modifier(
        display_name="Lock Capsule",
        type_id="LOCK_CAPSULE",
        class_name="LockModifierTiersModifier",
        player=True,
        stack_count=0
    )
    GRIP_CLAW = Modifier(
        display_name="On-hit item stealer",
        type_id="GRIP_CLAW",
        class_name="ContactHeldItemTransferChanceModifier",
        player=True,
        stack_count=0,
        requires_pokemon_id=True,
        type_pregen_args=[10]
    )
    GOLDEN_PUNCH = Modifier(
        display_name="On-hit money rewarded",
        type_id="GOLDEN_PUNCH",
        class_name="DamageMoneyRewardModifier",
        player=True,
        stack_count=0,
        requires_pokemon_id=True
    )
    EXP_BALANCE = Modifier(
        display_name="EXP Balancer",
        type_id="EXP_BALANCE",
        class_name="ExpBalancerModifier",
        player=True,
        stack_count=0
    )
    CANDY_JAR = Modifier(
        display_name="Rare Candy Booster",
        type_id="CANDY_JAR",
        class_name="LevelIncrementBoosterModifier",
        player=True,
        stack_count=0
    )
    AMULET_COIN = Modifier(
        display_name="More money from trainers",
        type_id="AMULET_COIN",
        class_name="MoneyMultiplierModifier",
        player=True,
        stack_count=0
    )
    BERRY_POUCH = Modifier(
        display_name="Chance to not lose berries",
        type_id="BERRY_POUCH",
        class_name="PreserveBerryModifier",
        player=True,
        stack_count=0
    )
    SHELL_BELL = Modifier(
        display_name="Heal-on-hit",
        type_id="SHELL_BELL",
        class_name="HitHealModifier",
        player=True,
        stack_count=0,
        requires_pokemon_id=True
    )
    SOUL_DEW = Modifier(
        display_name="Pokemon Nature Weight Modifier",
        type_id="SOUL_DEW",
        class_name="PokemonNatureWeightModifier",
        player=True,
        stack_count=0,
        requires_pokemon_id=True
    )
    WIDE_LENS = Modifier(
        display_name="Pokemon Accuracy Modifier",
        type_id="WIDE_LENS",
        class_name="PokemonMoveAccuracyBoosterModifier",
        player=True,
        stack_count=0,
        requires_pokemon_id=True,
        type_pregen_args=[5]
    )
    ATTACK_TYPE_BOOSTER = Modifier(
        display_name="Attack Type Booster Modifier",
        type_id="ATTACK_TYPE_BOOSTER",
        class_name="AttackTypeBoosterModifier",
        player=True,
        stack_count=0,
        requires_pokemon_id=True,
        requires_chance=True
    )
    EXP_SHARE = Modifier(
        display_name="EXP Share",
        type_id="EXP_SHARE",
        class_name="ExpShareModifier",
        player=True,
        stack_count=0
    )
    BASE_STAT_BOOSTER = Modifier(
        display_name="Base Stat Booster",
        type_id="BASE_STAT_BOOSTER",
        class_name="PokemonBaseStatModifier",
        player=True,
        stack_count=0,
        requires_pokemon_id=True,
        requires_chance=True
    )
    GOLDEN_POKEBALL = Modifier(
        display_name="Golden Pokeball",
        type_id="GOLDEN_POKEBALL",
        class_name="ExtraModifierModifier",
        player=True,
        stack_count=0
    )
    MEGA_BRACELET = Modifier(
        display_name="Mega Bracelet",
        type_id="MEGA_BRACELET",
        class_name="MegaEvolutionAccessModifier",
        player=True,
        stack_count=0
    )
    BERRY = Modifier(
        display_name="Berry Modifier",
        type_id="BERRY",
        class_name="BerryModifier",
        player=True,
        stack_count=0,
        requires_pokemon_id=True,
        requires_chance=True
    )
    DYNAMAX_BAND = Modifier(
        display_name="Dynamax Band",
        type_id="DYNAMAX_BAND",
        class_name="GigantamaxAccessModifier",
        player=True,
        stack_count=0
    )
