import os
import json

def parse_json_to_python(input_filepath: str, output_directory: str) -> None:
    """
    Parses a JSON file and generates a Python file with a class definition.

    Args:
    - input_filepath (str): Path to the input JSON file.
    - output_directory (str): Directory where the generated Python file should be saved.
    """
    try:
        with open(input_filepath, 'r') as infile:
            data = json.load(infile)

        # Determine the output filename based on the input filename
        filename = os.path.splitext(os.path.basename(input_filepath))[0]
        class_name = filename.title() + "Enum"
        output_filepath = os.path.join(output_directory, f"{filename.lower()}.py")

        # Generate the Python script content
        script_content = f"from enum import Enum\n\n"
        script_content += f"class {class_name}(Enum):\n"
        script_content += f"    {class_name}_DICT = {{\n"

        # Format each entry with new line and indentation
        for key, inner_dict in data.items():
            script_content += f"        '{key}': {{\n"
            for subkey, value in inner_dict.items():
                script_content += f"            '{subkey}': {value},\n"
            script_content += f"        }},\n"

        script_content += f"    }}\n"

        # Write the script content to a Python file
        with open(output_filepath, 'w') as outfile:
            outfile.write(script_content)

        print(f"Generated Python file for '{class_name}' saved to '{output_filepath}'.")

    except FileNotFoundError:
        print(f"Error: File '{input_filepath}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from '{input_filepath}'.")
    except Exception as e:
        print(f"Error: {e}")

def process_json_files(input_directory: str, output_directory: str) -> None:
    """
    Processes all JSON files in the given directory and converts them to Python files with class definitions.

    Args:
    - input_directory (str): Directory containing JSON files to process.
    - output_directory (str): Directory where the generated Python files should be saved.
    """
    try:
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Iterate over all JSON files in the input directory
        for filename in os.listdir(input_directory):
            if filename.endswith(".json"):
                input_filepath = os.path.join(input_directory, filename)

                # Parse JSON file and generate Python file
                parse_json_to_python(input_filepath, output_directory)

    except Exception as e:
        print(f"Error processing JSON files: {e}")

# Example usage:
input_directory = '../../data'
output_directory = './converted'

process_json_files(input_directory, output_directory)
