import random
import time
from typing import List, Dict, Any, Tuple

# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/JulianStiebler
# Date of release: 25.06.2024
# Last Edited: 25.06.2024

"""
This script provides functions to generate and manage eggs in a game environment,
including calculation of ID bounds, random ID generation, and egg data generation.

Features:
- Generates random IDs for different egg tiers and gacha types.
- Calculates ID bounds based on game constants.
- Generates eggs with specified properties including tier, gacha type, hatch waves, and timestamp.

Modules:
- random: Provides functions to generate random numbers, used for generating random egg IDs.
- time: Provides functions to work with time-related tasks, used for generating timestamps.
- typing: Provides type hints for better code clarity and type checking.

Workflow:
1. Define game constants like EGG_MULTIPLIER, GACHA_TYPES, and EGG_TIERS.
2. Use functions to calculate ID bounds for different egg tiers.
3. Generate random IDs within the calculated bounds, considering special cases like Manaphy eggs.
4. Generate eggs with specified properties such as tier, gacha type, hatch waves, and timestamp.

Modules/Librarys used and for what purpose exactly in each function:
- random: Provides functions for generating random numbers. Used in get_random_id() to generate random egg IDs.
- time: Provides functions for working with timestamps. Used in generate_eggs() to timestamp each generated egg.
- typing: Provides type hints for defining function argument types and return types. Used throughout for type annotations.

"""

EGG_MULTIPLIER: int = 1073741824
GACHA_TYPE: List[str] = ['MoveGacha', 'LegendaryGacha', 'ShinyGacha']
EGG_TIERS: List[str] = ['Common', 'Rare', 'Epic', 'Legendary', 'Manaphy']

def __eggGetIDBounds(tier: int) -> Tuple[int, int]:
    """
    Get the ID bounds for a given tier.

    Args:
        tier (int): The tier index.

    Returns:
        Tuple[int, int]: A tuple containing the start and end IDs.

    Raises:
        ValueError: If an invalid tier index is provided.
    """
    if tier < 1 or tier > len(EGG_TIERS):
        raise ValueError(f"Invalid tier index '{tier}'. Expected a value between 1 and {len(EGG_TIERS)}.")

    tierIndex = tier - 1  # Convert to 0-based index
    start = tierIndex * EGG_MULTIPLIER
    end = (tierIndex + 1) * EGG_MULTIPLIER - 1
    return max(start, 255), end

def __eggGetRandomId(start: int, end: int, manaphy: bool = False) -> int:
    """
    Get a random ID within the given range.

    Args:
        start (int): The start of the ID range.
        end (int): The end of the ID range.
        manaphy (bool): Whether the ID is for a Manaphy egg.

    Returns:
        int: The random ID.
    """
    if manaphy:
        return random.randrange(start, end + 1, 255)
    else:
        result: int = random.randint(start, end)
        result = result if result % 255 != 0 else result - 1
        return max(result, 1)

def constructEggs(tier: str, gachaType: str, hatchWaves: int, eggAmount: int, isShiny: bool, overrideHiddenAbility: bool) -> List[Dict[str, Any]]:
    """
    Construct a list of eggs with given properties.

    Args:
        tier (str): The tier of the eggs ('Common', 'Rare', 'Epic', 'Legendary', 'Manaphy').
        gachaType (str): The gacha type ('MoveGacha', 'LegendaryGacha', 'ShinyGacha').
        hatchWaves (int): The number of waves required to hatch.
        eggAmount (int): The number of eggs to construct.
        isShiny (bool): Whether the eggs should be shiny.
        overrideHiddenAbility (bool): Whether to override hidden ability.

    Returns:
        List[Dict[str, Any]]: A list of constructed egg dictionaries.
    """
    eggs = []
    tierIndex = EGG_TIERS.index(tier)

    for _ in range(eggAmount):
        eggId = __eggGetRandomId(*__eggGetIDBounds(tierIndex + 1), manaphy=(tier == 'Manaphy'))
        timestamp = int(time.time() * 1000)
        
        egg = {
            'id': eggId,
            'gachaType': GACHA_TYPE.index(gachaType),
            'hatchWaves': hatchWaves,
            'timestamp': timestamp,
            'tier': tierIndex,
            'isShiny': isShiny,
            'overrideHiddenAbility': overrideHiddenAbility
        }
        
        eggs.append(egg)

    return eggs
