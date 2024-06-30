@staticmethod
def data_iteratePokemon(species, pokemonNameByIDHelper, moveNamesByIDHelper, natureNamesByIDHelper):
    speciesDexID = str(species.get('species', 1)) # Needs to be string for comparison
    speciesDexName = pokemonNameByIDHelper.get(speciesDexID, f'Unknown Dex ID {speciesDexID}')
    speciesFormIndex = str(species.get('formIndex', None))
    # Fusions
    speciesFusionID = str(species.get('fusionSpecies', 0)) # Needs to be string for comparison
    speciesFusionName = pokemonNameByIDHelper.get(speciesFusionID, f'Unknown Fuse ID {speciesFusionID}')
    speciesFusionFormIndex = species.get('fusionFormIndex', None)
    speciesFusionLuck = species.get('fusionLuck', None)
    speciesFusionisShiny = species.get('fusionShiny', None)
    speciesFusionVariant = species.get('fusionVariant', None)

    # General info
    speciesIsShiny = species.get('shiny', False)
    speciesShinyVariant = species.get('variant', 0)
    speciesLuck = species.get('luck', 1)
    speciesLevel = species.get('level', 1)
    speciesMoves = [moveNamesByIDHelper[str(move["moveId"])] for move in species['moveset']]
    speciesNatureID = str(species.get('nature', 0))  # Assuming nature key is "nature" and default ID is 0
    speciesNatureName = natureNamesByIDHelper.get(speciesNatureID, "None")
    speciesIVs = species.get('ivs', 1)
    speciesHP = species.get('hp', 1)
    speciesPassive = species.get('passive', False)

    # Create a dictionary to hold all relevant information for the current Pokémon
    speciesInfo = {
        'id': speciesDexID,
        'name': speciesDexName.capitalize(),
        'formIndex': speciesFormIndex,
        'fusionID': speciesFusionID,
        'fusion': speciesFusionName,
        'fusionFormIndex': speciesFusionFormIndex,
        'fusionLuck': speciesFusionLuck,
        'fusionIsShiny': speciesFusionisShiny,
        'fusionVariant': speciesFusionVariant,
        'fusionStatus': 'Not fused' if speciesFusionID == '0' else f'Fused with {speciesFusionName}',
        'shiny': speciesIsShiny,
        'variant': speciesShinyVariant,
        'shinyStatus': f'Shiny {speciesShinyVariant}' if speciesIsShiny else 'Not Shiny',
        'luck': speciesLuck,
        'level': speciesLevel,
        'moves': speciesMoves,
        'natureID': speciesNatureID,
        'ivs': speciesIVs,
        'nature': speciesNatureName,
        'hp': speciesHP,
        'passive': speciesPassive,
        'data_ref': species
    }

    return speciesInfo

def data_iterateParty(slotData, pokemonNameByIDHelper, moveNamesByIDHelper, natureNamesByIDHelper):
    currentParty = []
    for pokemon in slotData['party']:
        speciesInfo = data_iteratePokemon(pokemon, pokemonNameByIDHelper, moveNamesByIDHelper, natureNamesByIDHelper)
        currentParty.append(speciesInfo)
        
    return currentParty