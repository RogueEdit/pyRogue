# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/JulianStiebler/
# Date of release: 13.06.2024 
# Last Edited: 28.06.2024

# Unlike the other code, reusing this in your own project is forbidden.

import os
import json
from typing import Any, List, Optional

# Define the Modifier class
class Modifier:
    def __init__(self, args: Optional[List[Any]], className: str, player: bool, stackCount: int, typeId: str, typePregenArgs: Optional[List[Any]] = None):
        self.args = self._sanitize_values(args)
        self.className = className
        self.player = player
        self.stackCount = 1  # Always set stackCount to 1
        self.typeId = typeId
        self.typePregenArgs = self._sanitize_values(typePregenArgs)

    def _sanitize_values(self, values: Optional[List[Any]]) -> Optional[List[Any]]:
        if values is None:
            return None
        return [None if (isinstance(v, (int, float)) and v > 30) else v for v in values]

    def fh_toDict(self) -> dict:
        data = {
            'args': self.args,
            'className': self.className,
            'player': self.player,
            'stackCount': self.stackCount,
            'typeId': self.typeId
        }
        if self.typePregenArgs is not None:
            data['typePregenArgs'] = self.typePregenArgs
        return data

    def fh_toPyCode(self, unique_name: str) -> str:
        argsStr = "None" if self.args is None else repr(self.args)
        typePregenArgs_str = "" if self.typePregenArgs is None else f", typePregenArgs={repr(self.typePregenArgs)}"
        return f"{unique_name} = Modifier(args={argsStr}, className={repr(self.className)}, player={self.player}, stackCount={self.stackCount}, typeId={repr(self.typeId)}{typePregenArgs_str})"

# Function to parse the game save file and extract modifiers
def parseGameSave(file_path: str) -> List[Modifier]:
    modifiers = []
    with open(file_path, 'r') as file:
        data = json.load(file)
        if 'modifiers' in data:
            for modifierData in data['modifiers']:
                modifier = parseModifier(modifierData)
                if modifier:
                    modifiers.append(modifier)
        if 'EnemyModifiers' in data:
            for modifierData in data['EnemyModifiers']:
                modifier = parseModifier(modifierData)
                if modifier:
                    modifiers.append(modifier)
    return modifiers

# Function to parse individual modifier data
def parseModifier(data: dict) -> Optional[Modifier]:
    if 'typeId' in data and 'className' in data and 'player' in data and 'stackCount' in data:
        args = data.get('args', None)
        className = data['className']
        player = data['player']
        stackCount = data['stackCount']
        typeId = data['typeId']
        typePregenArgs = data.get('typePregenArgs', None)
        
        return Modifier(args=args, className=className, player=player, stackCount=stackCount, typeId=typeId, typePregenArgs=typePregenArgs)
    return None

# Function to save extracted modifiers data to a JSON file
def saveExtracted(modifiers: List[Modifier], output_file: str):
    data = [modifier.fh_toDict() for modifier in modifiers]
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

# Custom sorting key function
def sorting_key(item: tuple) -> tuple:
    name, _ = item
    if any(char.isdigit() for char in name):
        parts = name.rsplit('_', 1)
        if parts[-1].isdigit():
            return (parts[0], int(parts[-1]))
    return (name, 0)

# Function to generate converted_.py with modifiers in Python code format
def f_generateConverted(modifiers: List[Modifier], output_file: str):
    unique_modifiers = {}
    for modifier in modifiers:
        typeId = modifier.typeId
        typePregenArgs = tuple(modifier.typePregenArgs) if modifier.typePregenArgs is not None else None
        if typeId not in unique_modifiers:
            unique_modifiers[typeId] = set()
        unique_modifiers[typeId].add(typePregenArgs)

    sortedModifier = []
    for typeId, typePregenArgs_set in unique_modifiers.items():
        for typePregenArgs in typePregenArgs_set:
            modifier = next(m for m in modifiers if m.typeId == typeId and (tuple(m.typePregenArgs) if m.typePregenArgs is not None else None) == typePregenArgs)
            uniqueName = typeId.replace('-', '_').upper()
            if typePregenArgs is not None:
                uniqueName += "".join(str(arg) for arg in typePregenArgs if arg is not None)
            sortedModifier.append((uniqueName, modifier))

    sortedModifier.sort(key=sorting_key)

    with open(output_file, 'w') as file:
        file.write("# This file contains converted modifiers\n")
        for uniqueName, modifier in sortedModifier:
            file.write(modifier.to_python_code(uniqueName) + "\n")

    print(f"Converted modifiers saved to '{output_file}'")

# Function to process all JSON files in the current directory
def processJSONFiles():
    currentDir = os.getcwd()
    JSONFiles = [file for file in os.listdir(currentDir) if file.endswith('.json') and not file.startswith('extracted_')]

    for jsonFile in JSONFiles:
        inputFIle = os.path.join(currentDir, jsonFile)
        extractedOutputFile = os.path.join(currentDir, f"extracted_{jsonFile}")
        converterOutputFile = os.path.join(currentDir, f"converted_{jsonFile.replace('.json', '.py')}")

        # Extract modifiers from input file
        modifiers = parseGameSave(inputFIle)

        # Save extracted modifiers to extracted_.json
        saveExtracted(modifiers, extractedOutputFile)

        # Generate converted_.py with modifiers in Python code format
        f_generateConverted(modifiers, converterOutputFile)

        print(f"Modifiers data extracted from '{jsonFile}', saved to '{extractedOutputFile}', and converted to '{converterOutputFile}'")

# Entry point of the script
def main():
    processJSONFiles()

if __name__ == "__main__":
    main()
