# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/M6D6M6A/
# -> Documentation: https://github.com/JulianStiebler
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
EGG_MULTIPLIER: int = 1073741824  # This constant is used for calculating ID bounds

# List of possible gacha types
GACHA_TYPES: List[str] = ['MOVE', 'LEGENDARY', 'SHINY']

# List of possible egg tiers
EGG_TIERS: List[str] = ['COMMON', 'RARE', 'EPIC', 'LEGENDARY', 'MANAPHY']

def get_id_bounds(tier: int) -> Tuple[int, int]:
    """
    Get the ID bounds for a given tier.

    Args:
        tier (int): The tier index.

    Returns:
        Tuple[int, int]: A tuple containing the start and end IDs.

    Example:
        start, end = get_id_bounds(2)
    """
    # Calculate the start and end IDs for the given tier
    start: int = tier * EGG_MULTIPLIER
    end: int = (tier + 1) * EGG_MULTIPLIER - 1
    return start or 255, end

def get_random_id(start: int, end: int, manaphy: bool = False) -> int:
    """
    Get a random ID within the given range.

    Args:
        start (int): The start of the ID range.
        end (int): The end of the ID range.
        manaphy (bool): Whether the ID is for a Manaphy egg.

    Returns:
        int: The random ID.

    Example:
        random_id = get_random_id(0, 1073741823)
    """
    if manaphy:
        # If the egg is Manaphy, simply return a random ID within the range
        return random.randrange(start, end + 1, 255)
    else:
        # If the egg is not Manaphy
        # Generate a random integer within the range
        result: int = random.randint(start, end)
        # Ensure the generated ID is not divisible by 255 (as it's reserved for Manaphy)
        result = result if result % 255 != 0 else result - 1
        # Ensure the ID is positive
        result = result if result > 0 else 1
        return result

def generate_eggs(tier: str, g_type: str, hatch_waves: int, num_eggs: int) -> List[Dict[str, int]]:
    """
    Generate eggs with the given properties.

    Args:
        tier (str): The tier of the eggs.
        g_type (str): The gacha type.
        hatch_waves (int): The number of hatch waves.
        num_eggs (int): The number of eggs to generate.

    Returns:
        List[Dict[str, int]]: A list of generated eggs.

    Example:
        eggs = generate_eggs('RARE', 'LEGENDARY', 3, 10)
    """
    # Check if the tier is for Manaphy eggs
    manaphy_flag: bool = tier == 'MANAPHY'
    # Calculate the start and end IDs based on the tier
    start, end = get_id_bounds(0 if manaphy_flag else EGG_TIERS.index(tier))
    
    eggs: List[Dict[str, int]] = []
    for _ in range(num_eggs):
        # Generate a random egg ID within the specified range
        egg_id: int = get_random_id(start, end, manaphy_flag)
        # Get the current timestamp
        timestamp: int = int(time.time() * 1000)
        # Create an egg dictionary with the generated properties
        eggs.append({
            'id': egg_id,
            'gachaType': GACHA_TYPES.index(g_type),
            'hatchWaves': hatch_waves,
            'timestamp': timestamp,
        })
    
    return eggs

if __name__ == '__main__':
    # Example of usage
    eggs = generate_eggs('RARE', 'LEGENDARY', 3, 10)
    print(eggs)
