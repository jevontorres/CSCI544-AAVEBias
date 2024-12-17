##script to extract INPUT row from csv
##input: ex finetuning json (instruction, input, output)
##output: txt file with just input column (the prompt incl. text)

import json

def extract_input_to_txt(fieldname, json_file, output_txt):
    try:
        # Open the JSON file
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)  # Load JSON data

        # Open the text file to write
        with open(output_txt, 'w', encoding='utf-8') as out:
            for obj in data:
                if fieldname in obj:  # Check if 'fieldname' field exists
                    out.write(obj[fieldname] + '\n')  # Write the input to the text file

        print(f"{fieldname} fields successfully extracted to {output_txt}")
    except FileNotFoundError:
        print(f"Error: The file {json_file} was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file {json_file} is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Usage example
# Replace 'input.json' with the path to your JSON file and 'output.txt' with your desired output file path
extract_input_to_txt("input", 'test_trimmed.json', 'test_trimmed.txt')