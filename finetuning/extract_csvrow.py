##script to take out the AAVE lines from a csv
##input: csv with AAVE Line column
##output: txt with AAVE lines

import csv

# Function to extract 'AAVE Line' column and write to txt
def extract_aave_line(rowname, input_csv, output_txt):
    try:
        with open(input_csv, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            
            # Ensure the column exists
            if rowname not in reader.fieldnames:
                print(f"Error: {rowname} column not found in the input CSV file.")
                return
            
            # Write to TXT file
            with open(output_txt, 'w') as txt_file:
                for row in reader:
                    if row[rowname]:  # Avoid empty values
                        txt_file.write(row[rowname] + '\n')
        
        print(f"{rowname} column has been successfully written to {output_txt}.")
    except FileNotFoundError:
        print(f"Error: File {input_csv} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'input.csv' and 'output.txt' with your filenames
extract_aave_line("Text",'sae_output_4_statistics_cleaned.csv', 'just_sae_lines.txt')