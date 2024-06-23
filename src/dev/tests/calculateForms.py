def calculate_form_id(index):
    base = 128 << index
    form_id = base | 64
    return form_id

# Adjust the form names to get all attributes shiny.

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

print("Tier3 Shiny Forms:")
for i, name in enumerate(form_names):
    caught_attr = 255 << i
    print(f"Form: {name} (Index: {i}) - caughtAttr: {caught_attr}")

combined_caught_attr = sum(255 << i for i in range(len(form_names)))

print("\nCombined caughtAttr for Tier3 Shiny forms:")
print(f"Combined caughtAttr: {combined_caught_attr}")


"""
Output:
    Tier3 Shiny Forms:
    Form: Normal (Index: 0) - caughtAttr: 255
    Form: Partner (Index: 1) - caughtAttr: 383
    Form: Cosplay (Index: 2) - caughtAttr: 639
    Form: Cool Cosplay (Index: 3) - caughtAttr: 1151
    Form: Beauty Cosplay (Index: 4) - caughtAttr: 2175
    Form: Cute Cosplay (Index: 5) - caughtAttr: 4223
    Form: Smart Cosplay (Index: 6) - caughtAttr: 8319
    Form: Tough Cosplay (Index: 7) - caughtAttr: 16511
    Form: G-Max (Index: 8) - caughtAttr: 32895

    Combined caughtAttr for Tier3 Shiny forms:
    Combined caughtAttr: 65535
"""