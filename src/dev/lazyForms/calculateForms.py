# Authors https://github.com/JulianStiebler/
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: None except Author
# Date of release: 24.06.2024 
# Last Edited: 28.06.2024

import json
from enum import Enum

# Constants from the flags
class DexAttr(Enum):
    NON_SHINY = 1
    SHINY = 2
    MALE = 4
    FEMALE = 8
    DEFAULT_VARIANT = 16
    VARIANT_2 = 32
    VARIANT_3 = 64
    DEFAULT_FORM = 128

# Load data from raw.json
with open('raw.json', 'r') as f:
    data = json.load(f)

# Function to compute caughtAttr for specific forms with VARIANT_3
def computeVariant3(pokeData, variantFlag, defaultFlag):
    caughtAttr = {}

    for pokeID, pokeInfo in pokeData['hasForms'].items():
        caughtAttr[pokeID] = {}

        for pokemon_name, forms in pokeInfo.items():
            caughtAttributes = {}
            combinedCaughtAttr = 0

            for formName in forms:
                formFlag = defaultFlag | (1 << (forms.index(formName) + 7))
                caughtAttr = 255 | formFlag | variantFlag
                caughtAttributes[formName] = caughtAttr - 128  # Adjust caught_attr to remove the extra 128

                # Update combined_caught_attr by ORing with the current form's caughtAttr
                combinedCaughtAttr |= caughtAttributes[formName] + 128  # Add 128 back before ORing

            # Assign the combined_caught_attr with an additional 128
            combinedCaughtAttr += 128

            # Add the entire caught_attrs dictionary directly
            caughtAttr[pokeID][pokemon_name] = caughtAttributes

            # Also add the combined_caught_attr at the top level of the Pokemon
            caughtAttr[pokeID]["Combined"] = combinedCaughtAttr+-128

    return caughtAttr

# Compute caughtAttr for each pokemon with VARIANT_3
flag3IDs = computeVariant3(data, DexAttr.VARIANT_3.value, DexAttr.DEFAULT_FORM.value)

# Write computed results to filled.json
with open('filled.json', 'w') as f:
    json.dump(flag3IDs, f, indent=4)

print("Data has been computed and saved to filled.json.")
