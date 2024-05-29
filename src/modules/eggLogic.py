import json
import random
import time

# Constants
EGG_MULTIPLIER = 1073741824

# Gacha types
GACHA_TYPES = ["MOVE", "LEGENDARY", "SHINY"]

# Egg tiers
EGG_TIERS = ["COMMON", "RARE", "EPIC", "LEGENDARY", "MANAPHY"]

# Function to generate valid ID ranges for a given tier
def get_id_bounds(tier):
    start = tier * EGG_MULTIPLIER
    end = (tier + 1) * EGG_MULTIPLIER - 1
    return start or 255, end

# Function to get a random ID within a specified range with step
def get_random_id(start, end, manaphy=False):
    if manaphy:
        return random.randrange(start, end + 1, 255)
    else:
        result = random.randint(start, end)
        result = result if result % 255 != 0 else result - 1
        result = result if result > 0 else 1
        return result

# Generator function
def generate_eggs(tier, g_type, hatch_waves, num_eggs):
    manaphy_flag = tier == "MANAPHY"
    start, end = get_id_bounds(0 if manaphy_flag else EGG_TIERS.index(tier))
    
    eggs = []
    for _ in range(num_eggs):
        egg_id = get_random_id(start, end, manaphy_flag)

        # Use current timestamp in milliseconds
        timestamp = int(time.time() * 1000)

        # Create egg object and append to list
        eggs.append({
            "id": egg_id,
            "gachaType": GACHA_TYPES.index(g_type),
            "hatchWaves": hatch_waves,
            "timestamp": timestamp,
        })
    
    return eggs

