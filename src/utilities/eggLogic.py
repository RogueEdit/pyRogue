# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/JulianStiebler
# Date of release: 06.06.2024
# Last Edited: 20.06.2024

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

import random
# Provides functions to generate random numbers, used here for generating random egg IDs.

import time
# Provides functions to work with time-related tasks, used here for generating timestamps.

from typing import List, Tuple, Dict
# Provides type hints for better code clarity and type checking.

# Constant from game source code
eggConstant: int = 1073741824  # This constant is used for calculating ID bounds

# List of possible gacha types
gachaTypes: List[str] = ['MoveGacha', 'LegendaryGacha', 'ShinyGacha']

# List of possible egg tiers
eggTiers: List[str] = ['Common', 'Rare', 'Epic', 'Legendary', 'Manaphy']

def getIDBoundarys(tier: int) -> Tuple[int, int]:
    """
    Get the ID bounds for a given tier.

    Args:
        tier (int): The tier index.

    Returns:
        Tuple[int, int]: A tuple containing the start and end IDs.

    Example:
        start, end = getIDBoundarys(2)
    """
    # Calculate the start and end IDs for the given tier
    start: int = tier * eggConstant
    end: int = (tier + 1) * eggConstant - 1
    return max(start, 255), end

def generateRandomID(start: int, end: int, manaphy: bool = False) -> int:
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

    result: int = random.randint(start, end)

    if result % 255 == 0:
        result -= 1

    return max(result, 1)

def constructEggs(tier: str, gachaType: str, hatchWaveCount: int, eggAmount: int, isShiny: bool, overrideHiddenAbility: bool) -> List[Dict[str, int]]:
    """
    Generate eggs with the given properties.

    Args:
        tier (str): The tier of the eggs.
        g_type (str): The gacha type.
        hatch_waves (int): The number of hatch waves.
        num_eggs (int): The number of eggs to generate.
        is_shiny (bool): Whether the egg is shiny.
        hidden_ability (bool): Whether the hidden ability is unlocked.

    Returns:
        List[Dict[str, int]]: A list of generated eggs.

    Example:
        eggs = constructEggs('Rare', 'LegendaryGacha', 3, 10, True, False)
    """
    isManaphy: bool = tier == 'Manaphy'
    start, end = getIDBoundarys(0 if isManaphy else eggTiers.index(tier))
    
    eggs: List[Dict[str, int]] = []
    for _ in range(eggAmount):
        egg_id: int = generateRandomID(start, end, isManaphy)
        timestamp: int = int(time.time() * 1000)
        
        egg: Dict[str, int] = {
            'id': egg_id,
            'gachaType': gachaTypes.index(gachaType),
            'hatchWaves': hatchWaveCount,
            'timestamp': timestamp,
            'tier': eggTiers.index(tier),
        }
        
        # Add optional fields based on the input
        if isShiny:
            egg['isShiny'] = isShiny
        if overrideHiddenAbility:
            egg['overrideHiddenAbility'] = overrideHiddenAbility
        
        eggs.append(egg)
    
    return eggs