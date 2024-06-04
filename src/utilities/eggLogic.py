# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood https://github.com/JulianStiebler/ https://github.com/M6D6M6A/
# Date of release: 04.06.2024 

import random
import time
from typing import List

# Define constants
EGG_MULTIPLIER = 1073741824  # This constant is used for calculating ID bounds

# List of possible gacha types
GACHA_TYPES = ['MOVE', 'LEGENDARY', 'SHINY']

# List of possible egg tiers
EGG_TIERS = ['COMMON', 'RARE', 'EPIC', 'LEGENDARY', 'MANAPHY']


def get_id_bounds(tier: int) -> tuple:
    """
    Get the ID bounds for a given tier.

    Args:
        tier (int): The tier index.

    Returns:
        tuple: A tuple containing the start and end IDs.
    """
    # Calculate the start and end IDs for the given tier
    start = tier * EGG_MULTIPLIER
    end = (tier + 1) * EGG_MULTIPLIER - 1
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
    """
    if manaphy:
        # If the egg is Manaphy, simply return a random ID within the range
        return random.randrange(start, end + 1, 255)
    else:
        # If the egg is not Manaphy
        # Generate a random integer within the range
        result = random.randint(start, end)
        # Ensure the generated ID is not divisible by 255 (as it's reserved for Manaphy)
        result = result if result % 255 != 0 else result - 1
        # Ensure the ID is positive
        result = result if result > 0 else 1
        return result


def generate_eggs(tier: str, g_type: str, hatch_waves: int, num_eggs: int) -> List[dict]:
    """
    Generate eggs with the given properties.

    Args:
        tier (str): The tier of the eggs.
        g_type (str): The gacha type.
        hatch_waves (int): The number of hatch waves.
        num_eggs (int): The number of eggs to generate.

    Returns:
        List[dict]: A list of generated eggs.
    """
    # Check if the tier is for Manaphy eggs
    manaphy_flag = tier == 'MANAPHY'
    # Calculate the start and end IDs based on the tier
    start, end = get_id_bounds(0 if manaphy_flag else EGG_TIERS.index(tier))
    
    eggs = []
    for _ in range(num_eggs):
        # Generate a random egg ID within the specified range
        egg_id = get_random_id(start, end, manaphy_flag)
        # Get the current timestamp
        timestamp = int(time.time() * 1000)
        # Create an egg dictionary with the generated properties
        eggs.append({
            'id': egg_id,
            'gachaType': GACHA_TYPES.index(g_type),
            'hatchWaves': hatch_waves,
            'timestamp': timestamp,
        })
    
    return eggs