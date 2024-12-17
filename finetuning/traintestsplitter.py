##script to split finetuning json into two parts, train and test
##input: finetuning json (instruction,input,output)
##output: 2 finetuning jsons, test and train

import json
import math

def split_json_file(input_file, output_file_train, output_file_test):
    split_ratio = 0.8

    try:
        # Read the input JSON file
        with open(input_file, 'r') as infile:
            data = json.load(infile)
        
        if isinstance(data, list):
            # Calculate the split points
            split_index = math.ceil(len(data) * split_ratio)
            train_chunk = data[:split_index]
            test_chunk = data[split_index:]

            # Write the first 80% to the first output JSON file
            with open(output_file_train, 'w') as output_train:
                json.dump(train_chunk, output_train, indent=4)

            # Write the last 20% to the second output JSON file
            with open(output_file_test, 'w') as output_test:
                json.dump(test_chunk, output_test, indent=4)
            
            print(f"First 80% saved to: {output_file_train} ({len(train_chunk)} objects)")
            print(f"Last 20% saved to: {output_file_test} ({len(test_chunk)} objects)")
        else:
            print("Input JSON is not a list of objects.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_file = "indiv_aave_to_sae_scores.json"
output_file_train = "train_trimmed.json"
output_file_test = "test_trimmed.json"

split_json_file(input_file, output_file_train, output_file_test)