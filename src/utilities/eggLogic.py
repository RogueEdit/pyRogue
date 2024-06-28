# Authors https://github.com/JulianStiebler/
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: None except Authors
# Date of release: 13.06.2024 
# Last Edited: 28.06.2024
# Based on: https://github.com/pagefaultgames/pokerogue/

"""
Source Code from https://github.com/pagefaultgames/pokerogue/ multiple files


Tier and Source Type Initialization:

    using eggOptions.tier to determine the _tier of the egg. If not provided, it falls back to Overrides.EGG_TIER_OVERRIDE or rolls a random tier using this.rollEggTier().
    _sourceType is set to eggOptions.sourceType or undefined.

Pulled Eggs:

    If eggOptions.pulled is true, you check for eggOptions.scene to potentially override the _tier using this.checkForPityTierOverrides().

ID Generation:

    _id is generated using eggOptions.id if provided or by calling Utils.randInt(EGG_SEED, EGG_SEED * this._tier).

Timestamp and Hatch Waves:

    _timestamp defaults to the current time if not provided in eggOptions.
    _hatchWaves is determined by eggOptions.hatchWaves or defaults to a tier-specific default using this.getEggTierDefaultHatchWaves().

Shiny, Variant, Species, and Hidden Ability:

    _isShiny is set based on eggOptions.isShiny, Overrides.EGG_SHINY_OVERRIDE, or randomly rolled.
    _variantTier is set similarly for variants.
    _species is determined by eggOptions.species or randomly rolled using this.rollSpecies().
    _overrideHiddenAbility is set to eggOptions.overrideHiddenAbility or defaults to false.

Species-Specific Handling:

    If eggOptions.species is provided, it overrides _tier and _hatchWaves. If the species has no variants, _variantTier is set to VariantTier.COMMON.

Egg Move Index:

    _eggMoveIndex defaults to a random value using this.rollEggMoveIndex() unless specified in eggOptions.

Pulled Egg Actions:

    If eggOptions.pulled is true, you increase pull statistics and add the egg to game data using this.increasePullStatistic() and this.addEggToGameData().

  constructor(eggOptions?: IEggOptions) {
    //if (eggOptions.tier && eggOptions.species) throw Error("Error egg can't have species and tier as option. only choose one of them.")

    this._tier = eggOptions.tier ?? (Overrides.EGG_TIER_OVERRIDE ?? this.rollEggTier());
    this._sourceType = eggOptions.sourceType ?? undefined;
    // If egg was pulled, check if egg pity needs to override the egg tier
    if (eggOptions.pulled) {
      // Needs this._tier and this._sourceType to work
      this.checkForPityTierOverrides(eggOptions.scene);
    }

    this._id = eggOptions.id ?? Utils.randInt(EGG_SEED, EGG_SEED * this._tier);

    this._sourceType = eggOptions.sourceType ?? undefined;
    this._hatchWaves = eggOptions.hatchWaves ?? this.getEggTierDefaultHatchWaves();
    this._timestamp = eggOptions.timestamp ?? new Date().getTime();

    // First roll shiny and variant so we can filter if species with an variant exist
    this._isShiny = eggOptions.isShiny ?? (Overrides.EGG_SHINY_OVERRIDE || this.rollShiny());
    this._variantTier = eggOptions.variantTier ?? (Overrides.EGG_VARIANT_OVERRIDE ?? this.rollVariant());
    this._species = eggOptions.species ?? this.rollSpecies(eggOptions.scene);

    this._overrideHiddenAbility = eggOptions.overrideHiddenAbility ?? false;

    // Override egg tier and hatchwaves if species was given
    if (eggOptions.species) {
      this._tier = this.getEggTierFromSpeciesStarterValue();
      this._hatchWaves = eggOptions.hatchWaves ?? this.getEggTierDefaultHatchWaves();
      // If species has no variant, set variantTier to common. This needs to
      // be done because species with no variants get filtered at rollSpecies but since the
      // species is set the check never happens
      if (!getPokemonSpecies(this.species).hasVariants()) {
        this._variantTier = VariantTier.COMMON;
      }
    }
    // Needs this._tier so it needs to be generated afer the tier override if bought from same species
    this._eggMoveIndex = eggOptions.eggMoveIndex ?? this.rollEggMoveIndex();
    if (eggOptions.pulled) {
      this.increasePullStatistic(eggOptions.scene);
      this.addEggToGameData(eggOptions.scene);
    }
  }


export const EGG_SEED = 1073741824;

// Rates for specific random properties in 1/x
const DEFAULT_SHINY_RATE = 128;
const GACHA_SHINY_UP_SHINY_RATE = 64;
const SAME_SPECIES_EGG_SHINY_RATE = 32;
const SAME_SPECIES_EGG_HA_RATE = 16;
const MANAPHY_EGG_MANAPHY_RATE = 8;

// 1/x for legendary eggs, 1/x*2 for epic eggs, 1/x*4 for rare eggs, and 1/x*8 for common eggs
const DEFAULT_RARE_EGGMOVE_RATE = 6;
const SAME_SPECIES_EGG_RARE_EGGMOVE_RATE = 3;
const GACHA_MOVE_UP_RARE_EGGMOVE_RATE = 3;


/** Egg options to override egg properties */
export interface IEggOptions {
  /** Id. Used to check if egg type will be manaphy (id % 204 === 0) */
  id?: number;
  /** Timestamp when this egg got created */
  timestamp?: number;
  /** Defines if the egg got pulled from a gacha or not. If true, egg pity and pull statistics will be applyed.
   * Egg will be automaticly added to the game data.
   * NEEDS scene eggOption to work.
   */
  pulled?: boolean;
  /** Defines where the egg comes from. Applies specific modifiers.
   * Will also define the text displayed in the egg list.
   */
  sourceType?: EggSourceType;
  /** Needs to be defined if eggOption pulled is defined or if no species or isShiny is degined since this will be needed to generate them. */
        export enum EggSourceType {
            GACHA_MOVE,
            GACHA_LEGENDARY,
            GACHA_SHINY,
            SAME_SPECIES_EGG,
            EVENT
        }
  scene?: BattleScene;
  /** Sets the tier of the egg. Only species of this tier can be hatched from this egg.
   * Tier will be overriden if species eggOption is set.
   */
  tier?: EggTier;
  /** Sets how many waves it will take till this egg hatches. */
  hatchWaves?: number;
  /** Sets the exact species that will hatch from this egg.
   * Needs scene eggOption if not provided.
   */
  species?: Species;
  /** Defines if the hatched pokemon will be a shiny. */
  isShiny?: boolean;
  /** Defines the variant of the pokemon that will hatch from this egg. If no variantTier is given the normal variant rates will apply. */
  variantTier?: VariantTier;
  /** Defines which egg move will be unlocked. 3 = rare egg move. */
  eggMoveIndex?: number;
  /** Defines if the egg will hatch with the hidden ability of this species.
   *  If no hidden ability exist, a random one will get choosen.
   */
  overrideHiddenAbility?: boolean
}
"""

import random
import time
from typing import List, Tuple, Dict

# Constant from game source code
EGG_SEED: int = 1073741824
GACHA_TYPES: List[str] = ['MoveGacha', 'LegendaryGacha', 'ShinyGacha', 'SAME_SPECIES_EGG', 'EVENT'],
EGG_TIERS: List[str] = ['Common', 'Rare', 'Epic', 'Legendary', 'Manaphy']

#From Sourcecode
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
        # Generate a random ID that is divisible by 204 within the specified range based on tier
        return random.randrange(start // 204 * 204, (end // 204 + 1) * 204, 204)
        """
            For better visibility thats whats happening in this oneliner
            idRangeStart = start // 204 * 204
            idRangeEnd = (end // 204 + 1) * 204 - 1
            return random.randrange(idRangeStart, idRangeEnd + 1, 204)
        """

    # Generate a regular random ID within the specified range
    result: int = random.randint(start, end)

    if result % 204 == 0:
        result -= 1

    return max(result, 1)

def constructEggs(tier: int, gachaType: int, hatchWaveCount: int, eggAmount: int, isShiny: bool = False, variantTier: int = 0) -> List[Dict[str, int]]:
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
            'gachaType': gachaType,
            'hatchWaves': int(hatchWaveCount),
            'timestamp': timestamp,
            'tier': tier-1,
        }
        if isShiny:
            egg['isShiny'] = isShiny
            egg['variantTier'] = int(variantTier)
        eggs.append(egg)
    
    return eggs
