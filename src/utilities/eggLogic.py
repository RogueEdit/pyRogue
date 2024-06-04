# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood https://github.com/JulianStiebler/ https://github.com/M6D6M6A/
# Date of release: 04.06.2024 

"""
Constants and Lists:

    EGG_MULTIPLIER: This constant is set to a large integer value (1073741824). It is used in calculating the ID bounds for different tiers of eggs.
    GACHA_TYPES: This list contains three strings representing different types of gacha: 'MOVE', 'LEGENDARY', and 'SHINY'.
    EGG_TIERS: This list contains five strings representing different tiers of eggs: 'COMMON', 'RARE', 'EPIC', 'LEGENDARY', and 'MANAPHY'.

get_id_bounds Function:

    This function takes a parameter tier, which is an integer representing the tier of the egg.
    It calculates the start and end IDs for the given tier based on the EGG_MULTIPLIER constant.
    The start ID is calculated as tier * EGG_MULTIPLIER, and the end ID is calculated as (tier + 1) * EGG_MULTIPLIER - 1.
    If the start ID is 0, it returns 255 as the start ID to avoid an ID of 0.
    It returns a tuple containing the start and end IDs.

get_random_id Function:

    This function takes three parameters: start, end, and manaphy.
    It generates a random ID within the given range (start to end).
    If manaphy is True, it ensures that the generated ID is a multiple of 255 by using random.randrange(start, end + 1, 255). This is specific logic related to Manaphy eggs.
    If manaphy is False, it generates a random ID and ensures that it's not a multiple of 255, and it's not less than or equal to 0.
    It returns the generated random ID.

generate_eggs Function:

    This function takes four parameters: tier, g_type, hatch_waves, and num_eggs.
    It generates a list of eggs based on the provided parameters.
    It determines the ID bounds for the given tier using the get_id_bounds function.
    It iterates num_eggs times, generating a random ID for each egg within the ID bounds.
    For each egg, it also generates a timestamp representing the current time in milliseconds.
    It constructs a dictionary for each egg containing the ID, gacha type index, hatch waves, and timestamp.
    It appends each egg dictionary to the eggs list.
    Finally, it returns the list of generated eggs.
    
"""

import random
import time
from typing import List, Optional
import random
import time
from typing import Optional
from enum import Enum, auto

EGG_MULTIPLIER = 1073741824

GACHA_TYPES = ['MOVE', 'LEGENDARY', 'SHINY']

EGG_TIERS = ['COMMON', 'RARE', 'EPIC', 'LEGENDARY', 'MANAPHY']


EGG_MULTIPLIER: int = 1073741824

GACHA_TYPES: List[str] = ['MOVE', 'LEGENDARY', 'SHINY']

EGG_TIERS: List[str] = ['COMMON', 'RARE', 'EPIC', 'LEGENDARY', 'MANAPHY']

def get_id_bounds(tier: int) -> tuple:
    """
    Get the ID bounds for a given tier.

    Args:
        tier (int): The tier index.

    Returns:
        tuple: A tuple containing the start and end IDs.
    """
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
        return random.randrange(start, end + 1, 255)
    else:
        result = random.randint(start, end)
        result = result if result % 255 != 0 else result - 1
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
    manaphy_flag = tier == 'MANAPHY'
    start, end = get_id_bounds(0 if manaphy_flag else EGG_TIERS.index(tier))
    
    eggs = []
    for _ in range(num_eggs):
        egg_id = get_random_id(start, end, manaphy_flag)

        timestamp = int(time.time() * 1000)
        eggs.append({
            'id': egg_id,
            'gachaType': GACHA_TYPES.index(g_type),
            'hatchWaves': hatch_waves,
            'timestamp': timestamp,
        })
    
    return eggs