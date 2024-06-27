import json

# Function to calculate form IDs based on index
def calculate_form_id(index):
    base = 128 << index
    form_id = base | 64
    return form_id

# Load data from raw.json
with open('raw.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Form names as given
form_names = [
    "Normal",
    "Partner",
    "Cosplay",
    "Cool Cosplay",
    "Beauty Cosplay",
    "Cute Cosplay",
    "Smart Cosplay",
    "Tough Cosplay",
    "G-Max"
]

# Dictionary to store calculated form IDs
form_ids = {}

# Iterate over each species in data
for species_id, species_data in data["hasForms"].items():
    species_id = int(species_id)
    species_form_ids = {}

    # Calculate form IDs for each form in the current species
    for form_name in species_data.keys():
        form_id = {}
        for i, name in enumerate(form_names):
            form_id[name] = calculate_form_id(i)
        species_form_ids[form_name] = form_id

    # Calculate combined caughtAttr for all forms of the species
    combined_caught_attr = sum(calculate_form_id(i) for i in range(len(form_names)))

    # Add form IDs and combined caughtAttr to the species
    species_form_ids["Combined"] = combined_caught_attr
    form_ids[species_id] = species_form_ids

# Create a new JSON structure with form IDs and combined values
result_json = {
    "hasForms": form_ids
}

# Output the result JSON to a file
with open('form_ids.json', 'w', encoding='utf-8') as outfile:
    json.dump(result_json, outfile, ensure_ascii=False, indent=4)

print("Form IDs and Combined values calculated and saved to form_ids.json")
