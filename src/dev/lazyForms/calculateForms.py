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
def compute_caught_attr_for_variant_3(pokemon_data, variant_flag, default_form_flag):
    pokemon_caught_attrs = {}

    for pokemon_id, pokemon_info in pokemon_data['hasForms'].items():
        pokemon_caught_attrs[pokemon_id] = {}

        for pokemon_name, forms in pokemon_info.items():
            caught_attrs = {}
            combined_caught_attr = 0

            for form_name in forms:
                form_flag = default_form_flag | (1 << (forms.index(form_name) + 7))
                caught_attr = 255 | form_flag | variant_flag
                caught_attrs[form_name] = caught_attr - 128  # Adjust caught_attr to remove the extra 128

                # Update combined_caught_attr by ORing with the current form's caughtAttr
                combined_caught_attr |= caught_attrs[form_name] + 128  # Add 128 back before ORing

            # Assign the combined_caught_attr with an additional 128
            combined_caught_attr += 128

            # Add the entire caught_attrs dictionary directly
            pokemon_caught_attrs[pokemon_id][pokemon_name] = caught_attrs

            # Also add the combined_caught_attr at the top level of the Pokemon
            pokemon_caught_attrs[pokemon_id]["Combined"] = combined_caught_attr+-128

    return pokemon_caught_attrs

# Compute caughtAttr for each pokemon with VARIANT_3
pokemon_caught_attrs_variant_3 = compute_caught_attr_for_variant_3(data, DexAttr.VARIANT_3.value, DexAttr.DEFAULT_FORM.value)

# Print the caughtAttr values for Pikachu
pikachu_data = pokemon_caught_attrs_variant_3["25"]["Pikachu"]
for form_name, caught_attr in pikachu_data.items():
    print(f"{form_name}: {caught_attr}")

# Write computed results to filled.json
with open('filled.json', 'w') as f:
    json.dump(pokemon_caught_attrs_variant_3, f, indent=4)

print("Data has been computed and saved to filled.json.")
