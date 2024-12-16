import pandas as pd
import json

def csv_to_json(input_csv, output_json):
    # Load the CSV file
    df = pd.read_csv(input_csv)
    
    # Ensure necessary columns are present
    required_columns = [
        'Text','AAVE Line', 'Intelligence', 'Kindness', 'Sophistication',
        'Aggression', 'Emotional', 'Laziness', 'Factual'
    ]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    
    # List to store JSON objects
    json_data = []
    
    # Loop through each row and construct the JSON structure
    for _, row in df.iterrows():
        # Extract values from the row
        aave_line = row['AAVE Line']
        sae_line = row['Text']
        scores = {
            "Intelligence": row['Intelligence'],
            "Kindness": row['Kindness'],
            "Sophistication": row['Sophistication'],
            "Aggression": row['Aggression'],
            "Emotional": row['Emotional'],
            "Laziness": row['Laziness'],
            "Factual": row['Factual']
        }
        
        # Format the "output" string
        output = "\n".join([f"* {key}: {value}" for key, value in scores.items()])
        
        # Create the JSON structure for this row
        json_entry = {
            "instruction": "You are a helpful assistant, assisting with a research project on Standard American English and African American Vernacular English.",
            "input": f'Give me a score from 1-10 about the type of person who says "{aave_line}" in terms of intelligence, kindness, sophistication, aggression, emotional, laziness, and factual. Just give me the scores.',
            "output": output
        }
        
        # Append to the list
        json_data.append(json_entry)
    
    # Write to JSON file
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

# Example usage
csv_to_json('sae_output_4_statistics_cleaned.csv', 'indiv_aave_to_sae_scores.json')