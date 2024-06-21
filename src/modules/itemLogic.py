# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/JulianStiebler/
# Date of release: 06.06.2024 
# Last edited: 20.06.2024 - https://github.com/JulianStiebler/

from dataclasses import dataclass
from typing import Optional, List, Any
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
    EXP_SHARE = Modifier(
        display_name="EXP Share",
        type_id="EXP_SHARE",
        class_name="ExpShareModifier",
        player=True,
        stack_count=5
    )
    SUPER_EXP_CHARM = Modifier(
        display_name="Super Exp Charm",
        type_id="SUPER_EXP_CHARM",
        class_name="ExpBoosterModifier",
        player=True,
        stack_count=25,
        requires_chance=True,
        type_pregen_args=[60]
    )
    EXP_CHARM = Modifier(
        display_name="Exp Charm",
        type_id="EXP_CHARM",
        class_name="ExpBoosterModifier",
        player=True,
        stack_count=68,

        stack_count=31,
        requires_pokemon_id=True,
        type_pregen_args=[5]
    )
    BASE_STAT_BOOSTER_1 = Modifier(
        display_name="Base Stat Booster",
        type_id="BASE_STAT_BOOSTER",
        class_name="PokemonBaseStatModifier",
        player=True,
        stack_count=2,
        requires_pokemon_id=True,
        type_pregen_args=[1]
    )
    BASE_STAT_BOOSTER_0 = Modifier(
        display_name="Base Stat Booster",
        type_id="BASE_STAT_BOOSTER",
        class_name="PokemonBaseStatModifier",
        player=True,
        stack_count=31,
        requires_pokemon_id=True,
        type_pregen_args=[0]
    )
    MEGA_BRACELET = Modifier(
        display_name="Mega Bracelet",
        type_id="MEGA_BRACELET",
        class_name="MegaEvolutionAccessModifier",
        player=True,
        stack_count=1
    )
    BERRY_10 = Modifier(
        display_name="Berry Modifier",
        type_id="BERRY",
        class_name="BerryModifier",
        player=True,
        stack_count=2,
        requires_pokemon_id=True,
        type_pregen_args=[10]
    )
    EXP_BALANCE = Modifier(
        display_name="Exp Balance",
        type_id="EXP_BALANCE",
        class_name="ExpBalanceModifier",
        player=True,
        stack_count=4
    )
    AMULET_COIN = Modifier(
        display_name="Amulet Coin",
        type_id="AMULET_COIN",
        class_name="MoneyMultiplierModifier",
        player=True,
        stack_count=5
    )
    DYNAMAX_BAND = Modifier(
        display_name="Dynamax Band",
        type_id="DYNAMAX_BAND",
        class_name="GigantamaxAccessModifier",
        player=True,
        stack_count=1
    )
    BASE_STAT_BOOSTER_3 = Modifier(
        display_name="Base Stat Booster",
