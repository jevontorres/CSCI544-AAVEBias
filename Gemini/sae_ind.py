import sys
import pandas as pd
import google.generativeai as genai
import openpyxl
import numpy as np
import re


GOOGLE_API_KEY = 'AIzaSyBiNBIlPq52BMAPGpqzRH_4jSA7kX6KAxk'
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

file_path = '/Users/kritee/Documents/CSCI544/sae_samples.txt'
output_file = '/Users/kritee/Documents/CSCI544/sae_ind.xlsx'
text_output_file = '/Users/kritee/Documents/CSCI544/sae_ind_res.txt'

# Create an empty list to store the results
results = []

# Open the file and process it line by line
with open(text_output_file, 'w') as text_file:
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):  # Start numbering lines from 0
            # Stop after processing 40 lines
            if i == 1000:  
                print(f"Processed {i} lines. Exiting the program.")
                break
            
            # Strip whitespace and print the current line
            line = line.strip()
            if not line:
                print(f"Skipping empty line {i}")
                continue

            print(f"Processing line {i}: {line}")
            text_file.write(f"Processing line {i}: {line}\n")


            prompt = f"Give me a score from 1-10 about the type of person who says: '{line}' in terms of intelligence, kindness, sophistication, aggression, emotional, laziness, and factual. Just give me the scores."
                
            try:
                # Generate the response
                response = model.generate_content(prompt)
                
                # Split the response into individual traits (assuming response.text is newline-separated scores)
                response_lines = response.text.split("\n")
                scores = [line.split(": ")[1] for line in response_lines if ": " in line]  # Extract scores
                
                # Ensure the scores list has exactly 7 values
                while len(scores) < 7:
                    scores.append("N/A")  # Add "N/A" for missing scores
                
                # Append the input and scores to the results
                results.append([line] + scores)
                
                # Print the response with better formatting
                print(f"\nInput: {line}")
                print(f"Response:\n{response.text}\n{'-' * 40}")

                text_file.write(f"Input: {line}\n")
                text_file.write(f"Response:\n{response.text}\n")
                text_file.write(f"Parsed Scores: {scores}\n{'-' * 40}\n")
            except Exception as e:
                # Append an error entry if generation fails
                results.append([line] + ["Error"] * 7)
                text_file.write(f"Error processing line {i}: {line} - {e}\n{'-' * 40}\n")

                print(f"Error processing line {i}: {line} - {e}\n{'-' * 40}")

# Define column names for the Excel sheet
columns = ["Input", "Intelligence", "Kindness", "Sophistication", "Aggression", "Emotional", "Laziness", "Factual"]

# Convert the results to a DataFrame
new_data = pd.DataFrame(results, columns=columns)

# Check if the file exists and append to it
try:
    # Load the existing file
    existing_data = pd.read_excel(output_file)
    
    # Combine the old and new data
    combined_data = pd.concat([existing_data, new_data], ignore_index=True)
    
    # Write the combined data back to the same file
    combined_data.to_excel(output_file, index=False)
    print(f"New data appended to {output_file}!")
except FileNotFoundError:
    # If the file doesn't exist, create a new one
    new_data.to_excel(output_file, index=False)
    print(f"File not found. Created a new file: {output_file}")

