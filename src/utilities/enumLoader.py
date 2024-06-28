# Authors https://github.com/JulianStiebler https://github.com/claudiunderthehood
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
            pokemon_id_by_name (Optional[dict]): Dictionary for Pokemon IDs by name.
            biomes_by_id (Optional[dict]): Dictionary for biomes by ID.
            moves_by_id (Optional[dict]): Dictionary for moves by ID.
            natures_data (Optional[dict]): Dictionary for natures data.
            vouchers_data (Optional[dict]): Dictionary for vouchers data.
            natureSlot_data (Optional[dict]): Dictionary for nature slot data.

        Modules:
            - typing: Provides type hints for better code clarity and type checking.
        """
        self.starterNameByID: Optional[Dict[str, int]] = None
        self.biomesByID: Optional[Dict[str, int]] = None
        self.movesByID: Optional[Dict[str, int]] = None
        self.natureData: Optional[Dict[str, int]] = None
        self.voucherData: Optional[Dict[str, int]] = None
        self.natureDataSlots: Optional[Dict[str, int]] = None
        self.noPassiveIDs: Optional[Dict[str, int]] = None
        self.hasFormIDs: Optional[Dict[str, int]] = None

    def __f_loadData(self) -> None:
        """
        Load data from JSON files located in the directory specified by config.dataDirectory.

        Raises:
            Exception: If there is an error loading the data files.

        Example:
            loader = EnumLoader()
            loader.__load_data()

        Modules:
            - json: Provides functionalities to work with JSON data for reading and writing.
            - modules.config: Contains configuration settings, specifically for directory paths.
            - utilities.cFormatter: Custom formatter for colored printing and logging.
        """
        try:
            dataDir: str = config.dataDirectory

            with open(f'{dataDir}/starter.json') as f:
                self.starterNameByID = json.load(f)

            with open(f'{dataDir}/biomes.json') as f:
                self.biomesByID = json.load(f)

            with open(f'{dataDir}/moves.json') as f:
                self.movesByID = json.load(f)

            with open(f'{dataDir}/natures.json') as f:
                self.natureData = json.load(f)

            with open(f'{dataDir}/vouchers.json') as f:
                self.voucherData = json.load(f)
            
            with open(f'{dataDir}/natureSlot.json') as f:
                self.natureDataSlots = json.load(f)

            with open(f'{dataDir}/achievements.json') as f:
                self.achievementsData = json.load(f)

            with open(f'{dataDir}/pokemon.json') as f:
                self.pokemonNameByID = json.load(f)

            with open(f'{dataDir}/noPassive.json') as f:
                self.noPassiveIDs = json.load(f)

            with open(f'{dataDir}/formIDs.json') as f:
                self.hasFormIDs = json.load(f)

            
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in enumLoader.__f_loadData(). {e}', isLogging=True)

    def __f_createENUMFromDict(self, data_dict: Dict[str, int], enum_name: str) -> Enum:
        """
        Create an Enum from a dictionary.

        Args:
            data_dict (dict): The dictionary to convert to an Enum.
            enum_name (str): The name of the Enum.

        Returns:
            Enum: The created Enum.

        Example:
            loader = EnumLoader()
            pokemon_enum = loader.__create_enum_from_dict({'PIKACHU': 25}, 'PokemonEnum')

        Modules:
            - enum: Provides support for enumerations, a set of symbolic names bound to unique, constant values.
        """
        enum_cls: Enum = Enum(enum_name, {key: value for key, value in data_dict.items()})
        return enum_cls

    def f_convertToEnums(self) -> Tuple[Enum, Enum, Enum, Enum, Enum, Enum]:
        """
        Convert loaded data to Enums.

        Returns:
            self.pokemonIDByName, self.biomesByID, self.movesByID, self.voucherData, self.natureData, self.natureDataSlots, self.achievementsData
            tuple: A tuple containing the created Enums for Pokemon IDs, biomes, moves, natures, vouchers, and nature slots.

        Example:
            loader = EnumLoader()
            enums = loader.convert_to_enums()
            pokemon_enum = enums[0]  # Access PokemonEnum

        Modules:
            - json: Provides functionalities to work with JSON data for reading and writing.
            - enum: Provides support for enumerations, a set of symbolic names bound to unique, constant values.
            - modules.config: Contains configuration settings, specifically for directory paths.
            - utilities.cFormatter: Custom formatter for colored printing and logging.
        """
        self.__f_loadData()

        self.starterNameByID = self.__f_createENUMFromDict(self.starterNameByID['dex'], 'StarterEnum')
        self.biomesByID = self.__f_createENUMFromDict(self.biomesByID['biomes'], 'BiomesEnum')
        self.movesByID = self.__f_createENUMFromDict(self.movesByID['moves'], 'MovesEnum')
        self.voucherData = self.__f_createENUMFromDict(self.voucherData['vouchers'], 'VouchersEnum')
        self.natureData = self.__f_createENUMFromDict(self.natureData['natures'], 'NaturesEnum')
        self.natureDataSlots = self.__f_createENUMFromDict(self.natureDataSlots['natureSlot'], 'NaturesSlotEnum')
        self.achievementsData = self.__f_createENUMFromDict(self.achievementsData['achvUnlocks'], 'AchievementsEnum')
        self.pokemonNameByID = self.__f_createENUMFromDict(self.pokemonNameByID['dex'], 'PokemonEnum')
        self.noPassiveIDs = self.__f_createENUMFromDict(self.noPassiveIDs['noPassive'], 'NoPassiveEnum')
        self.hasFormIDs = self.__f_createENUMFromDict(self.hasFormIDs['hasForms'], 'HasFormsEnum')

        return (self.starterNameByID, self.biomesByID, self.movesByID, self.voucherData, 
                self.natureData, self.natureDataSlots, self.achievementsData, self.pokemonNameByID,
                self.noPassiveIDs, self.hasFormIDs)
