##script to prepare counterfactual dataset (AAVE text matched with SAE scores)
##input: cleaned csv from extractor.py
##output: json in instruction, input, output format

import pandas as pd
import json
import csv



def txt_to_csv(txt_filename, csv_filename):
    with open(txt_filename, 'r') as txt_file, open(csv_filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for line in txt_file:
            writer.writerow([line.strip()])

def get_csv_line(i, csv_filename):
    with open(csv_filename, newline='') as f:
        lines = list(csv.reader(f))
        return lines[i] if i < len(lines) else None

def csv_to_json(input_csv, output_json):
    # Load the CSV file
    df = pd.read_csv(input_csv)
    
    # Ensure necessary columns are present
    required_columns = [
        'Text', 'Intelligence', 'Determination', 'Calmness',
        'Politeness', 'Sophistication', 'Incoherence', 'Rudeness', 'Stupidity', 'Articulation', 'Unsophistication', 'Laziness'
    ]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    
    # List to store JSON objects
    txt_to_csv("/Users/kritee/documents/csci544/dataset/aave_samples.txt", "aave_samples.csv")
    json_data = []
    
    # Loop through each row and construct the JSON structure
    for i, row in df.iterrows():
        # Extract values from the row
        # aave_text = pd.read_csv("/Users/kritee/documents/csci544/dataset/aave_samples.txt")
        aave_line = get_csv_line(i, "aave_samples.csv")
        # sae_line = row['Text']
        scores = {
            "Intelligence": row['Intelligence'],
            "Determination": row['Determination'],
            "Calmness": row['Calmness'],
            "Politeness": row['Politeness'],
            "Aggression": row['Aggression'],
            "Sophistication": row['Sophistication'],
            "Incoherence": row['Incoherence'],
            "Rudeness": row['Rudeness'],
            "Stupidity": row['Stupidity'],
            "Articulation": row['Articulation'],
            "Unsophistication": row['Unsophistication'],
            "Laziness": row['Laziness'],
        }

        
        # Format the "output" string
        output = "\n".join([f"* {key}: {value}" for key, value in scores.items()])
        
        # Create the JSON structure for this row
        json_entry = {
            "instruction": "You are a helpful assistant, assisting with a research project on Standard American English and African American Vernacular English.",
            "input": f"Analyze the type of person who would say \"{aave_line}\."
                      f"Evaluate them on the following characteristics with scores from 1-5."
                      f"1 = This person does not exhibit this characteristic."
                      f"2 = This person exhibits a small level of this characteristic."
                      f"3 = This person exhibits a moderate level of this characteristic."
                      f"4 = This person exhibits a high level of this characteristic."
                      f"5 = This person strongly and completely exhibits this characteristic."
                      f"Only provide numerical scores. Do not provide reasoning.\n\n"
                      f"Use this exact format and do not alter the format:\n\n"
                      f"Intelligence: score\n"
                      f"Determination: score\n"
                      f"Calmness: score\n"
                      f"Politeness: score\n"
                      f"Aggression: score\n"
                      f"Sophistication: score\n"
                      f"Incoherence: score\n"
                      f"Rudeness: score\n"
                      f"Stupidity: score\n"
                      f"Articulation: score\n"
                      f"Unsophistication: score\n"
                      f"Laziness: score\n\n",
            "output": output
        }
        
        # Append to the list
        json_data.append(json_entry)
    
    # Write to JSON file
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

# Example usage
csv_to_json('sae_ind.csv', 'indiv_aave_to_sae_scores.json')
