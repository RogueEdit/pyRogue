# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood https://github.com/JulianStiebler/ https://github.com/M6D6M6A/
# Date of release: 04.06.2024 


import random
import time

EGG_MULTIPLIER = 1073741824

GACHA_TYPES = ["MOVE", "LEGENDARY", "SHINY"]

EGG_TIERS = ["COMMON", "RARE", "EPIC", "LEGENDARY", "MANAPHY"]

def get_id_bounds(tier):
    start = tier * EGG_MULTIPLIER
    end = (tier + 1) * EGG_MULTIPLIER - 1
    return start or 255, end

def get_random_id(start, end, manaphy=False):
    if manaphy:
        return random.randrange(start, end + 1, 255)
    else:
        result = random.randint(start, end)
        result = result if result % 255 != 0 else result - 1
        result = result if result > 0 else 1
        return result

def generate_eggs(tier, g_type, hatch_waves, num_eggs):
    manaphy_flag = tier == "MANAPHY"
    start, end = get_id_bounds(0 if manaphy_flag else EGG_TIERS.index(tier))
    
    eggs = []
    for _ in range(num_eggs):
        egg_id = get_random_id(start, end, manaphy_flag)

        timestamp = int(time.time() * 1000)
        eggs.append({
            "id": egg_id,
            "gachaType": GACHA_TYPES.index(g_type),
            "hatchWaves": hatch_waves,
            "timestamp": timestamp,
        })
    
    return eggs

