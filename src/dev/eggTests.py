import random
import time
from typing import List, Dict, Tuple

# Constant from game source code
EGG_SEED: int = 1073741824

# List of possible gacha types & List of possible egg tiers
GACHA_TYPES: List[str] = ['MoveGacha', 'LegendaryGacha', 'ShinyGacha', 'SAME_SPECIES_EGG', 'EVENT']
eggTiers: List[str] = ['Common', 'Rare', 'Epic', 'Legendary', 'Manaphy%Old', 'Manaphy%New']

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
    start: int = tier * EGG_SEED
    end: int = (tier + 1) * EGG_SEED - 1
    return max(start, 255), end

def generateRandomID(start: int, end: int, tier: int) -> int:
    """
    Get a random ID within the given range or modulo 204 for tier 4 (Manaphy).

    Args:
        start (int): The start of the ID range.
        end (int): The end of the ID range.
        tier (int): The tier index.

    Returns:
        int: The random ID.
    """
    if tier < 4:
        # Generate a regular random ID within the specified range for tiers 0 to 3
        result: int = random.randint(start, end)
        if result % 204 == 0:
            result -= 1
        return max(result, 1)
    elif tier == 4:
        return random.randrange(start, end + 1, 255)
    elif tier == 5:
        # Generate a random ID that is divisible by 204 within the specified range
        idRangeMin = start // 204 * 204
        idRangeMax = (end // 204 + 1) * 204 - 1
        return random.randrange(idRangeMin, idRangeMax + 1, 204)
    else:
        raise ValueError("Invalid tier index. Must be between 0 and 5 inclusive.")

def constructEggs(tier: int, gachaType: str, hatchWaveCount: int, eggAmount: int, isShiny: bool, variantTier: bool) -> List[Dict[str, int]]:
    """
    Generate eggs with the given properties.

    Args:
        tier (int): The tier of the eggs.
        g_type (int): The gacha type.
        hatch_waves (int): The number of hatch waves.
        num_eggs (int): The number of eggs to generate.
        is_shiny (bool): Whether the egg is shiny.
        hidden_ability (bool): Whether the hidden ability is unlocked.

    Returns:
        List[Dict[str, int]]: A list of generated eggs.

    Example:
        eggs = constructEggs(1, 2, 3, 10, True, False)
    """
    isManaphy: bool = tier == 4
    start, end = getIDBoundarys(0 if isManaphy else tier)
    
    eggs: List[Dict[str, int]] = []
    for _ in range(eggAmount):
        eggID: int = generateRandomID(start, end, isManaphy)
        timestamp: int = int(time.time() * 1000)
        
        egg: Dict[str, int] = {
            'id': eggID,
            'gachaType': GACHA_TYPES.index(gachaType),
            'hatchWaves': hatchWaveCount,
            'timestamp': timestamp,
            'tier': tier,
        }
        if variantTier:
            egg['variantTier'] = 3
        if isShiny:
            egg['isShiny'] = isShiny
        eggs.append(egg)
    
    return eggs

def testEggIDGeneration(tier: int, eggAmount: int = 100):
    """
    Test the egg ID generation to ensure IDs are within the expected bounds.

    Args:
        tier (int): The tier of the eggs.
        eggAmount (int): The number of eggs to generate for testing.

    Returns:
        None
    """
    gachaType = random.choice(GACHA_TYPES)
    hatchWaveCount = random.randint(1, 10)
    isShiny = random.choice([True, False])
    variantTier = random.choice([True, False])
    
    eggs = constructEggs(tier, gachaType, hatchWaveCount, eggAmount, isShiny, variantTier)
    start, end = getIDBoundarys(tier)
    tierStr = eggTiers[tier] if tier < len(eggTiers) else f"Tier {tier}"
    for egg in eggs:
        eggID = egg['id']
        if not (start <= eggID <= end):
            print(f"Error: Egg ID {eggID} is out of bounds for tier {tierStr} (expected between {start} and {end})")
        else:
            print(f"Egg ID {eggID} is within bounds for tier {tierStr} (between {start} and {end})")

# Test the ID generation for each tier
for tier in range(len(eggTiers)):
    print(f"Testing egg ID generation for tier {tier} ({eggTiers[tier]})")
    testEggIDGeneration(tier)
    print("\n")
