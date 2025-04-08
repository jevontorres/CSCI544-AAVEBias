import sys
import pandas as pd
import google.generativeai as genai
import openpyxl
import numpy as np
import re

# add api key
# GOOGLE_API_KEY = 
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-2.0-flash')

file_path_2 = '/Users/kritee/Documents/CSCI544/dataset/sae_samples.txt'
output_file = '/Users/kritee/Documents/CSCI544/dataset/sae_ind.xlsx'
text_output_file = '/Users/kritee/Documents/CSCI544/dataset/sae_ind.txt'

# Create an empty list to store the results
results = []

# Open the file and process it line by line
with open(text_output_file, 'w') as text_file:
    with open(file_path_2, 'r') as file:
        for i, line in enumerate(file):
            # Stop after processing 1000 lines
            if i == 2020:
                print(f"Processed {i} lines. Exiting the program.")
                break
            
            # Strip whitespace and skip empty lines
            line = line.strip()
            if not line:
                print(f"Skipping empty line {i}")
                continue

            print(f"Processing line {i}: {line}")
            text_file.write(f"Processing line {i}: {line}\n")
            
            prompt = (f"Analyze the type of person who would say \"{line}\."
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
                      f"Laziness: score\n\n"
                )


            try:
                # Generate the response
                response = model.generate_content(prompt)

                # Ensure we store the original sentence
                original_sentence = line  # Store the original input
              
                extracted_scores = {
                    "Intelligence": "N/A",
                    "Determination": "N/A",
                    "Calmness": "N/A",
                    "Politeness": "N/A",
                    "Aggression": "N/A",
                    "Sophistication": "N/A",
                    "Incoherence": "N/A",
                    "Rudeness": "N/A",
                    "Stupidity": "N/A",
                    "Articulation": "N/A",
                    "Unsophistication": "N/A",
                    "Laziness": "N/A"
                }

                # Loop through response lines and extract the scores correctly
                for resp_line in response.text.split("\n"):
                    match = re.match(r"^(Intelligence|Determination|Calmness|Politeness|Aggression|Sophistication|Incoherence|Rudeness|Stupidity|Articulation|Unsophistication|Laziness):\s*(\d+)", resp_line)
                    if match:
                        trait, score = match.groups()
                        extracted_scores[trait] = score  # Store the score for the correct trait

                # Append the original input sentence and extracted scores to results
                results.append([original_sentence] + list(extracted_scores.values()))

                # Print and log response
                print(f"\nInput: {original_sentence}")
                print(f"Response:\n{response.text}\n{'-' * 40}")

                text_file.write(f"Input: {original_sentence}\n")
                text_file.write(f"Response:\n{response.text}\n")
                text_file.write(f"Parsed Scores: {list(extracted_scores.values())}\n{'-' * 40}\n")

            except Exception as e:
                # Handle errors
                results.append([line] + ["Error"] * 7)
                text_file.write(f"Error processing line {i}: {line} - {e}\n{'-' * 40}\n")
                print(f"Error processing line {i}: {line} - {e}\n{'-' * 40}")

# Define column names for the Excel sheet
columns = ["Text", "Intelligence", "Determination", "Calmness", "Politeness", "Aggression",
           "Sophistication", "Incoherence", "Rudeness", "Stupidity", "Articulation",
           "Unsophistication", "Laziness"]

# Convert results to a DataFrame
new_data = pd.DataFrame(results, columns=columns)

# Check if the file exists and append to it
try:
    existing_data = pd.read_excel(output_file)

    # Concatenate old and new data
    combined_data = pd.concat([existing_data, new_data], ignore_index=True)

    # Save back to Excel
    combined_data.to_excel(output_file, index=False)
    print(f"New data appended to {output_file}!")

except FileNotFoundError:
    # If file does not exist, create a new one
    new_data.to_excel(output_file, index=False)
    print(f"File not found. Created a new file: {output_file}")
