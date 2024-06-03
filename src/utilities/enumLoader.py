# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood https://github.com/JulianStiebler/
# Date of release: 04.06.2024 


import json

from enum import Enum, auto

class EnumLoader:
    def __init__(self):
        self.pokemon_id_by_name = None
        self.biomes_by_id = None
        self.moves_by_id = None
        self.natures_data = None
        self.vouchers_data = None
        self.natureSlot_data = None

    def __load_data(self):
        with open("./data/pokemon.json") as f:
            self.pokemon_id_by_name = json.load(f)

        with open("./data/biomes.json") as f:
            self.biomes_by_id = json.load(f)

        with open("./data/moves.json") as f:
            self.moves_by_id = json.load(f)

        with open("./data/natures.json") as f:
            self.natures_data = json.load(f)

        with open("./data/vouchers.json") as f:
            self.vouchers_data = json.load(f)
        
        with open("./data/natureSlot.json") as f:
            self.natureSlot_data = json.load(f)

    def __create_enum_from_dict(self, data_dict, enum_name):
        enum_cls = Enum(enum_name, {key: value for key, value in data_dict.items()})
        return enum_cls

    def convert_to_enums(self) -> tuple:

        self.__load_data()

        self.pokemon_id_by_name = self.__create_enum_from_dict(self.pokemon_id_by_name["dex"], "PokemonEnum")
        self.biomes_by_id = self.__create_enum_from_dict(self.biomes_by_id["biomes"], "BiomesEnum")
        self.moves_by_id = self.__create_enum_from_dict(self.moves_by_id["moves"], "MovesEnum")
        self.natures_data = self.__create_enum_from_dict(self.natures_data["natures"], "NaturesEnum")
        self.vouchers_data = self.__create_enum_from_dict(self.vouchers_data["vouchers"], "VouchersEnum")
        self.natureSlot_data = self.__create_enum_from_dict(self.natureSlot_data["natureSlot"], "NaturesSlotEnum")

        return self.pokemon_id_by_name, self.biomes_by_id, self.moves_by_id, self.natures_data, self.vouchers_data, self.natureSlot_data
    


