# Authors: https://github.com/JulianStiebler https://github.com/claudiunderthehood
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: None except Authors
# Date of release: 06.06.2024
# Last Edited: 28.06.2024
# Based on: https://github.com/pagefaultgames/pokerogue/

"""
This script provides functionalities to load data from JSON files and convert them into Enums.
It includes the capability to handle Pokemon IDs, biomes, moves, natures, vouchers, and nature slots.

Modules:
- utilities: Custom module for colored printing and logging functionalities (cFormatter and Color).
- modules: Contains configuration settings (config).
- json: Provides functionalities to work with JSON data.
- enum: Provides support for enumerations, a set of symbolic names bound to unique, constant values.

Workflow:
1. Initialize the EnumLoader class.
2. Load data from JSON files located in a specified directory.
3. Convert loaded data to Enums.
4. Return the created Enums.
"""

from utilities import cFormatter, Color
# Custom module for colored printing and logging functionalities.

from modules import config
# Contains configuration settings, specifically for directory paths.

import json
# Provides functionalities to work with JSON data for reading and writing.

from enum import Enum
# Provides support for enumerations, a set of symbolic names bound to unique, constant values.

from typing import Optional, Tuple, Dict
# Provides type hints for better code clarity and type checking.

class EnumLoader:
    def __init__(self) -> None:
        """
        Initialize the EnumLoader object.

        Attributes:
            starterNameByID (Optional[Dict[str, int]]): Dictionary for starter IDs by name.
            biomesByID (Optional[Dict[str, int]]): Dictionary for biomes by ID.
            movesByID (Optional[Dict[str, int]]): Dictionary for moves by ID.
            natureData (Optional[Dict[str, int]]): Dictionary for natures data.
            voucherData (Optional[Dict[str, int]]): Dictionary for vouchers data.
            natureDataSlots (Optional[Dict[str, int]]): Dictionary for nature slot data.
            noPassiveIDs (Optional[Dict[str, int]]): Dictionary for no passive IDs.
            hasFormIDs (Optional[Dict[str, int]]): Dictionary for IDs that have forms.
            speciesNameByID (Optional[Dict[str, int]]): Dictionary for species names by ID.
            achievementsData (Optional[Dict[str, int]]): Dictionary for achievements data.
        """
        self.starterNameByID: Optional[Dict[str, int]] = None
        self.biomesByID: Optional[Dict[str, int]] = None
        self.movesByID: Optional[Dict[str, int]] = None
        self.natureData: Optional[Dict[str, int]] = None
        self.voucherData: Optional[Dict[str, int]] = None
        self.natureDataSlots: Optional[Dict[str, int]] = None
        self.noPassiveIDs: Optional[Dict[str, int]] = None
        self.hasFormIDs: Optional[Dict[str, int]] = None
        self.speciesNameByID: Optional[Dict[str, int]] = None
        self.achievementsData: Optional[Dict[str, int]] = None
        self.eggTypesData: Optional[Dict[str, int]] = None

    def __f_loadData(self) -> None:
        """
        Load data from JSON files located in the directory specified by config.dataDirectory.

        Raises:
            Exception: If there is an error loading the data files.

        Example:
            loader = EnumLoader()
            loader.__f_loadData()
        """
        try:
            dataDir: str = config.dataDirectory

            with open(f'{dataDir}/starter.json') as f:
                self.starterNameByID: Dict[str, int] = json.load(f)

            with open(f'{dataDir}/biomes.json') as f:
                self.biomesByID: Dict[str, int] = json.load(f)

            with open(f'{dataDir}/moves.json') as f:
                self.movesByID: Dict[str, int] = json.load(f)

            with open(f'{dataDir}/natures.json') as f:
                self.natureData: Dict[str, int] = json.load(f)

            with open(f'{dataDir}/vouchers.json') as f:
                self.voucherData: Dict[str, int] = json.load(f)
            
            with open(f'{dataDir}/natureSlot.json') as f:
                self.natureDataSlots: Dict[str, int] = json.load(f)

            with open(f'{dataDir}/achievements.json') as f:
                self.achievementsData: Dict[str, int] = json.load(f)

            with open(f'{dataDir}/species.json') as f:
                self.speciesNameByID: Dict[str, int] = json.load(f)

            with open(f'{dataDir}/noPassive.json') as f:
                self.noPassiveIDs: Dict[str, int] = json.load(f)

            with open(f'{dataDir}/hasForms.json') as f:
                self.hasFormIDs: Dict[str, int] = json.load(f)

            with open(f'{dataDir}/eggTypes.json') as f:
                self.eggTypesData: Dict[str, int] = json.load(f)

        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in enumLoader.__f_loadData(). {e}', isLogging=True)

    def __f_createENUMFromDict(self, dataDict: Dict[str, int], enumName: str) -> Enum:
        """
        Create an Enum from a dictionary.

        Args:
            dataDict (Dict[str, int]): The dictionary to convert to an Enum.
            enumName (str): The name of the Enum.

        Returns:
            Enum: The created Enum.

        Example:
            loader = EnumLoader()
            speciesEnum = loader.__f_createENUMFromDict({'PIKACHU': 25}, 'SpeciesEnum')
        """
        enumClass: Enum = Enum(enumName, {key: value for key, value in dataDict.items()})
        return enumClass

    def f_convertToEnums(self) -> Tuple[Enum, Enum, Enum, Enum, Enum, Enum, Enum, Enum, Enum, Enum]:
        """
        Convert loaded data to Enums.

        Returns:
            Tuple[Enum, Enum, Enum, Enum, Enum, Enum, Enum, Enum, Enum, Enum]: 
            A tuple containing the created Enums for starter names, biomes, moves, vouchers, natures, nature slots,
            achievements, species names, no passive IDs, and IDs with forms.

        Example:
            loader = EnumLoader()
            enums = loader.f_convertToEnums()
            StarterEnum = enums[0]  # Access StarterEnum
        """
        self.__f_loadData()

        self.starterNameByID: Dict[str, int] = self.__f_createENUMFromDict(self.starterNameByID["dex"], 'StarterEnum')
        self.biomesByID: Dict[str, int] = self.__f_createENUMFromDict(self.biomesByID["biomes"], 'BiomesEnum')
        self.movesByID: Dict[str, int] = self.__f_createENUMFromDict(self.movesByID["moves"], 'MovesEnum')
        self.voucherData: Dict[str, int] = self.__f_createENUMFromDict(self.voucherData["vouchers"], 'VouchersEnum')
        self.natureData: Dict[str, int] = self.__f_createENUMFromDict(self.natureData["natures"], 'NaturesEnum')
        self.natureDataSlots: Dict[str, int] = self.__f_createENUMFromDict(self.natureDataSlots["natureSlot"], 'NaturesSlotEnum')
        self.achievementsData: Dict[str, int] = self.__f_createENUMFromDict(self.achievementsData["achvUnlocks"], 'AchievementsEnum')
        self.speciesNameByID: Dict[str, int] = self.__f_createENUMFromDict(self.speciesNameByID["dex"], 'PokemonEnum')
        self.noPassiveIDs: Dict[str, int] = self.__f_createENUMFromDict(self.noPassiveIDs["noPassive"], 'NoPassiveEnum')
        self.hasFormIDs: Dict[str, int] = self.__f_createENUMFromDict(self.hasFormIDs["hasForms"], 'HasFormsEnum')
        self.eggTypesData: Dict[str, int] = self.__f_createENUMFromDict(self.eggTypesData["eggTypes"], 'eggtypeEnum')


        return (self.starterNameByID, self.biomesByID, self.movesByID, self.voucherData, 
                self.natureData, self.natureDataSlots, self.achievementsData, self.speciesNameByID,
                self.noPassiveIDs, self.hasFormIDs, self.eggTypesData)
