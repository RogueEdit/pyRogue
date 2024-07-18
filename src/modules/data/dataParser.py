# Authors https://github.com/JulianStiebler/
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: None except Authors
# Date of release: 06.06.2024 
# Last Edited: 28.06.2024

# Unlike the other code, reusing this in your own project is forbidden.

import json
from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Any, Dict, Union
from modules.config import dataDirectory
from colorama import Fore, Style

def __createEnum(name, values):
    return Enum(name, values)

def __modifiySpeciesName(name):
    return name.replace('_', ' ').title()

with open(f'{dataDirectory}/hasForms.json') as f:
    hasForms = json.load(f)["hasForms"]

with open(f'{dataDirectory}/species.json') as f:
    dexEnum = json.load(f)["dex"]

with open(f'{dataDirectory}/noPassive.json') as f:
    noPassive = json.load(f)["noPassive"]

with open(f'{dataDirectory}/starter.json') as f:
    startersList = json.load(f)["dex"]

Dex = __createEnum('Dex', {name.capitalize(): id_ for name, id_ in dexEnum.items()})
noPassiveSet = {int(id_) for id_ in noPassive.keys()}
startersSet = {dexEnum[name] for name in startersList}

class DexAttr(Enum):
    NON_SHINY = 1
    SHINY = 2
    MALE = 4
    FEMALE = 8
    VARIANT_1 = 16
    VARIANT_2 = 32
    VARIANT_3 = 64
    DEFAULT_FORM = 128

@dataclass
class Modifier:
    args: List[Optional[Union[int, bool]]]
    className: Optional[str]
    player: Optional[bool]
    stackCount: Optional[int]
    typeId: Optional[str]
    typePregenArgs: Optional[List[Optional[int]]]

    def toDict(self):
        return asdict(self)

@dataclass
class ModifierEnemyData:
    modifiers: List[Optional[Modifier]]

    def toDict(self):
        return asdict(self)

@dataclass
class ModifierPlayerData:
    modifiers: List[Optional[Modifier]]

@dataclass
class Move:
    moveId: Optional[int] = None
    ppUp: Optional[int] = None
    ppUsed: Optional[int] = None
    virtual: Optional[bool] = None

    def toDict(self):
        return asdict(self)

@dataclass
class PartySummonData:
    abilitiesApplied: Optional[Any] = None
    ability: Optional[int] = None
    abilitySuppressed: Optional[bool] = None
    battleStats: List[Optional[int]] = field(default_factory=lambda: [None, None, None, None, None, None, None])
    disabledMove: Optional[int] = None
    disabledTurns: Optional[int] = None
    moveQueue: Optional[Any] = None
    tags: Optional[Any] = None
    types: Optional[Any] = None

    def toDict(self):
        return asdict(self)

@dataclass
class PartyDetails:
    abilityIndex: Optional[int] = None
    boss: Optional[bool] = None
    exp: Optional[int] = None
    formIndex: Optional[int] = None
    friendship: Optional[int] = None
    fusionFormIndex: Optional[int] = None
    fusionLuck: Optional[int] = None
    fusionShiny: Optional[int] = None
    fusionSpecies: Optional[int] = None
    fusionVariant: Optional[int] = None
    gender: Optional[int] = None
    hp: Optional[int] = None
    id: Optional[int] = None
    ivs: List[Optional[int]] = field(default_factory=lambda: [None, None, None, None, None, None])
    level: Optional[int] = None
    levelExp: Optional[int] = None
    luck: Optional[int] = None
    metBiome: Optional[int] = None
    metLevel: Optional[int] = None
    moveset: List[Move] = field(default_factory=lambda: [Move(), Move(), Move(), Move()])
    nature: Optional[int] = None
    natureOverride: Optional[int] = None
    passive: Optional[bool] = None
    pauseEvolutions: Optional[bool] = None
    player: Optional[bool] = None
    pokeball: Optional[int] = None
    pokerus: Optional[bool] = None
    shiny: Optional[bool] = None
    species: Optional[int] = None
    stats: List[Optional[int]] = field(default_factory=lambda: [None, None, None, None, None, None])
    summonData: PartySummonData = field(default_factory=PartySummonData)
    variant: Optional[int] = None

    def toDict(self):
        return asdict(self)

@dataclass
class PartyPlayer:
    partyInfo: Optional[PartyDetails] = field(default_factory=PartyDetails)
    partyData: Optional[PartySummonData] = field(default_factory=PartySummonData)

    def toDict(self):
        return asdict(self)

@dataclass
class PartyEnemy:
    partyInfo: Optional[PartyDetails] = field(default_factory=PartyDetails)
    partyData: Optional[PartySummonData] = field(default_factory=PartySummonData)

    def toDict(self):
        return asdict(self)

@dataclass
class SpeciesDexData:
    seenAttr: int = 0
    caughtAttr: int = 0
    natureAttr: int = 0
    seenCount: int = 0
    caughtCount: int = 0
    hatchedCount: int = 0
    ivs: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0, 0])

    def toDict(self):
        return asdict(self)

@dataclass
class SpeciesStarterData:
    moveset: Optional[List[int]] = field(default_factory=lambda: [])
    eggMoves: Optional[int] = None
    candyCount: Optional[int] = 0
    friendship: Optional[int] = 0
    abilityAttr: Optional[int] = 0
    passiveAttr: Optional[int] = 0
    valueReduction: Optional[int] = 0
    classicWinCount: Optional[int] = 0

    def toDict(self):
        return asdict(self)

@dataclass
class SpeciesForm:
    name: str
    variant1: Optional[int] = None
    variant2: Optional[int] = None
    variant3: Optional[int] = None
    nonShiny: Optional[int] = None
    index: int = 0

    def toDict(self):
        return asdict(self)

@dataclass
class Species:
    name: str
    dex: int
    forms: List[SpeciesForm]
    hasPassive: bool
    isStarter: bool
    isNormalForm: bool

    # User Data
    # put starterData and dexData here

    def __post_init__(self):
        self.formMap = {form.name: form for form in self.forms}

    def getFormAttribute(self, formName: str, attribute: str) -> Optional[int]:
        form = self.formMap.get(formName)
        if form:
            return getattr(form, attribute, None)
        else:
            return None
        
    def toDict(self):
        return asdict(self)

def computeVariant(speciesData, variantFlag, defaultFlag, variantAdjustment):
    caughtAttr = {}

    for speciesID, speciesInfo in speciesData.items():
        caughtAttr[speciesID] = {}

        for speciesName, forms in speciesInfo.items():
            if speciesName == "isNormalForm":
                continue

            formAttributes = {}
            combinedCaughtAttr = {
                "variant1": 31,
                "variant2": 63,
                "variant3": 127,
                "nonShiny": 255
            }

            for index, formName in enumerate(forms):
                formFlag = defaultFlag | (1 << (index + 7))
                formCaughtAttr = 255 | formFlag | variantFlag

                adjustedFormCaughtAttr = formCaughtAttr - variantAdjustment
                formAttributes[formName] = adjustedFormCaughtAttr

                combinedCaughtAttr["variant1"] |= adjustedFormCaughtAttr
                combinedCaughtAttr["variant2"] |= adjustedFormCaughtAttr
                combinedCaughtAttr["variant3"] |= adjustedFormCaughtAttr
                combinedCaughtAttr["nonShiny"] |= adjustedFormCaughtAttr

            caughtAttr[speciesID][speciesName] = formAttributes

        caughtAttr[speciesID]["Combined"] = {
            "variant1": combinedCaughtAttr["variant1"] + 128,
            "variant2": combinedCaughtAttr["variant2"] + 128,
            "variant3": combinedCaughtAttr["variant3"] + 128,
            "nonShiny": combinedCaughtAttr["nonShiny"] + 128
        }

    return caughtAttr

variant1CaughtAttr = computeVariant(hasForms, DexAttr.VARIANT_1.value, DexAttr.DEFAULT_FORM.value, 224)
variant2CaughtAttr = computeVariant(hasForms, DexAttr.VARIANT_2.value, DexAttr.DEFAULT_FORM.value, 192)
variant3CaughtAttr = computeVariant(hasForms, DexAttr.VARIANT_3.value, DexAttr.DEFAULT_FORM.value, 128)
nonShinyCaughtAttr = computeVariant(hasForms, DexAttr.NON_SHINY.value, DexAttr.DEFAULT_FORM.value, 255)

specieses = []
speciesDict = {}

for speciesName, speciesId in dexEnum.items():
    modifiedName = __modifiySpeciesName(speciesName)
    hasPassive = int(speciesId) not in noPassiveSet
    isStarter = speciesId in startersSet
    speciesIdString = str(speciesId)

    forms = []
    isNormalForm = False
    if speciesIdString in hasForms:
        formNames = hasForms[speciesIdString].get(modifiedName, [])
        isNormalForm = hasForms[speciesIdString].get("isNormalForm", False)
        combinedCaughtAttr = {
            "variant1": 31,
            "variant2": 63,
            "variant3": 127,
            "nonShiny": 255
        }
        for index, formName in enumerate(formNames):
            form = SpeciesForm(
                name=formName,
                variant1=variant1CaughtAttr[speciesIdString][modifiedName][formName],
                variant2=variant2CaughtAttr[speciesIdString][modifiedName][formName],
                variant3=variant3CaughtAttr[speciesIdString][modifiedName][formName],
                nonShiny=nonShinyCaughtAttr[speciesIdString][modifiedName][formName],
                index=index
            )
            forms.append(form)
            combinedCaughtAttr["variant1"] |= form.variant1
            combinedCaughtAttr["variant2"] |= form.variant2
            combinedCaughtAttr["variant3"] |= form.variant3
            combinedCaughtAttr["nonShiny"] |= form.nonShiny

        # Add the imaginary "Combined" form with proper variant values
        forms.append(SpeciesForm(
            name="Combined",
            variant1=combinedCaughtAttr["variant1"] + 128,
            variant2=combinedCaughtAttr["variant2"] + 128,
            variant3=combinedCaughtAttr["variant3"] + 128,
            nonShiny=combinedCaughtAttr["nonShiny"] + 128,
            index=len(forms)
        ))

    species = Species(
        name=modifiedName,
        dex=int(speciesId),
        forms=forms,
        hasPassive=hasPassive,
        isStarter=isStarter,
        isNormalForm=isNormalForm
    )
    specieses.append(species)
    speciesDict[speciesName] = species
    speciesDict[speciesId] = species

@dataclass
class SessionData:
    seed: Optional[str] = None
    playTime: Optional[int] = 0
    gameMode: Optional[int] = 0
    party: Optional[PartyPlayer] = field(default_factory=PartyPlayer)
    enemyParty: Optional[PartyEnemy] = field(default_factory=PartyEnemy)
    playerModifier: Optional[ModifierPlayerData] = field(default_factory=ModifierPlayerData)
    enemyModifier: Optional[ModifierEnemyData] = field(default_factory=ModifierEnemyData)
    arena: Optional[Dict[str, Union[int, None]]] = field(default_factory=lambda: {"biome": 0, "tags": None})
    pokeballCounts: Optional[Dict[str, Optional[int]]] = field(default_factory=lambda: {"0": 5, "1": 0, "2": 0, "3": 0, "4": 0})
    money: Optional[int] = None
    score: Optional[int] = None
    victoryCount: Optional[int] = None
    faintCount: Optional[int] = None
    reviveCount: Optional[int] = None
    waveIndex: Optional[int] = None
    battleType: Optional[int] = None
    trainer: Optional[int] = None
    gameVersion: Optional[str] = None
    timestamp: Optional[int] = None
    challenges: Optional[Dict[str, None]] = None

    def toDict(self):
        return asdict(self)


@dataclass
class TrainerData:
    trainerId: Optional[int] = None
    secretId: Optional[int] = None
    gender: Optional[int] = None
    dexData: Optional[SpeciesDexData] = field(default_factory=SpeciesDexData)
    starterData: Optional[SpeciesStarterData] = field(default_factory=SpeciesStarterData)
    starterMoveData: Optional[List[int]] = field(default_factory=lambda: [])
    starterEggMoveData: Optional[List[int]] = field(default_factory=lambda: [])
    gameStats: Optional[Dict[str, Optional[int]]] = None
    unlocks: Optional[Dict[str, Optional[bool]]] = None
    achvUnlocks: Optional[Dict[str, Optional[int]]] = None
    voucherUnlocks: Optional[Dict[str, Optional[int]]] = None
    voucherCounts: Optional[Dict[str, Optional[int]]] = None
    eggs: Optional[Dict[str, None]] = None
    eggPity: Optional[List[int]] = field(default_factory=lambda: [0, 0, 0, 0])
    unlockPity: Optional[List[int]] = field(default_factory=lambda: [0, 0, 0, 0])
    gameVersion: Optional[int] = None
    timestamp: Optional[int] = None

    def toDict(self):
        return asdict(self)



def fh_getCombinedIDs(includeStarter=True, onlyNormalForms=True):
    combinedFormIds = []

    for species in specieses:
        if (includeStarter or not species.isStarter) and (not onlyNormalForms or species.isNormalForm):
            for form in species.forms:
                if form.name == "Combined":
                    combinedFormIds.append({
                        "speciesID": species.dex,
                        "speciesName": species.name,
                        "formName": form.name,
                        "caughtAttr": form.variant3,
                        "formIndex": form.index
                    })

    return combinedFormIds

@staticmethod
def data_iterateParty(slotData, speciesNameByIDHelper, moveNamesByIDHelper, natureNamesByIDHelper):
    currentParty = []
    pokeballList = {
        0: "Pokeball",
        1: "Great Ball",
        2: "Hyper Ball",
        3: "Rogue Ball",
        4: "Master Ball",
        5: "Luxury Ball"
    }
    for object in slotData.get("party", []):  # Use .get() to avoid KeyError if "party" doesn't exist
        # Define IDs and indices
        speciesDexID = str(object.get('species', 1))
        speciesFusionID = str(object.get('fusionSpecies', 0))
        speciesFormIndex = int(object.get('formIndex', 0))
        speciesFusionFormIndex = int(object.get('fusionFormIndex', 0))

        # Get base names
        speciesDexName = speciesNameByIDHelper.get(speciesDexID, f'Unknown Dex ID {speciesDexID}')
        speciesFusionName = speciesNameByIDHelper.get(speciesFusionID, f'Unknown Fuse ID {speciesFusionID}')

        # Modify names based on form index
        if speciesFormIndex > 0 and int(speciesDexID) in speciesDict and len(speciesDict[int(speciesDexID)].forms) > speciesFormIndex:
            speciesFormName = speciesDict[int(speciesDexID)].forms[speciesFormIndex].name
            speciesDexName = f'{speciesFormName} {speciesDexName}'

        if speciesFusionFormIndex > 0 and speciesFusionID != '0' and int(speciesFusionID) in speciesDict and len(speciesDict[int(speciesFusionID)].forms) > speciesFusionFormIndex:
            speciesFusionFormName = speciesDict[int(speciesFusionID)].forms[speciesFusionFormIndex].name
            speciesFusionName = f'{speciesFusionFormName} {speciesFusionName}'

        # General fusion info
        speciesFusionLuck = object.get('fusionLuck', None)
        speciesFusionisShiny = object.get('fusionShiny', None)
        speciesFusionVariant = object.get('fusionVariant', None)

        # General species info
        speciesIsShiny = object.get('shiny', False)
        speciesShinyVariant = object.get('variant', 0)
        speciesLuck = object.get('luck', 1)
        speciesLevel = object.get('level', 1)
        
        # Ensure moveset is a list and handle missing move IDs
        speciesMoves = [moveNamesByIDHelper.get(str(move.get("moveId", 0)), "Unknown Move") for move in object.get("moveset", [])]
        
        speciesNatureID = str(object.get('nature', 0))
        speciesNatureName = natureNamesByIDHelper.get(speciesNatureID, "None")
        speciesIVs = object.get('ivs', 1)
        speciesHP = object.get('hp', 1)
        speciesPassive = object.get('passive', False)
        
        # Check if the species has a passive ability
        if int(speciesDexID) in speciesDict and hasattr(speciesDict[int(speciesDexID)], 'hasPassive') and speciesDict[int(speciesDexID)].hasPassive:
            speciesPassiveStatus = object.get('passive', False)
        else:
            speciesPassiveStatus = 'Not available'
        
        speciesPokerus = object.get('pokerus', False)
        speciesPokeball = object.get('pokeball', 0)
        
        # Handle missing Pokeball types
        speciesPokeballStatus = pokeballList.get(speciesPokeball, "Unknown Pokeball")

        speciesInfo = {
            'id': speciesDexID,
            'fusionID': speciesFusionID,
            'formIndex': speciesFormIndex,
            'fusionFormIndex': speciesFusionFormIndex,
            'name': speciesDexName.title(),

            'fusion': speciesFusionName.title(),
            'fusionLuck': speciesFusionLuck,
            'fusionIsShiny': speciesFusionisShiny,
            'fusionVariant': speciesFusionVariant,

            'shiny': speciesIsShiny,
            'variant': speciesShinyVariant,
            'luck': speciesLuck,
            'level': speciesLevel,
            'moves': speciesMoves,
            'natureID': speciesNatureID,
            'nature': speciesNatureName,
            'ivs': speciesIVs,
            'hp': speciesHP,
            'passive': speciesPassive,
            'passiveStatus': speciesPassiveStatus,
            'pokerus': speciesPokerus,
            'pokeball': speciesPokeball,

            'pokeballStatus': speciesPokeballStatus,
            'fusionStatus': '' if speciesFusionID == '0' else f'Fused with {Fore.YELLOW}{speciesFusionName.title()}{Style.RESET_ALL}',
            'shinyStatus': f'Shiny {speciesShinyVariant + 1}' if speciesIsShiny else 'Not Shiny',
            'luckCount': speciesLuck if speciesFusionID == '0' else (speciesLuck + (speciesFusionLuck if speciesFusionLuck is not None else 0)),
            'data_ref': object
        }

        currentParty.append(speciesInfo)

    return currentParty