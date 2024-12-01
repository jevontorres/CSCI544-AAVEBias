import re
import csv

def extract_scores(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    comparisons = content.split('--------------------------------------------------')
    results = []
    traits = ['Intelligence', 'Kindness', 'Sophistication', 'Aggression', 'Emotional', 'Laziness', 'Factual']

    for comparison in comparisons:
        aave_scores = {trait: '' for trait in traits}
        sae_scores = {trait: '' for trait in traits}

        # Find the start of the AAVE and SAE sections
        aave_start = comparison.find('AAVE')
        sae_start = comparison.find('SAE')

        if aave_start != -1:
            # Extract AAVE scores
            aave_part = comparison[aave_start:]
            for trait in traits:
                aave_pattern = rf'{trait}:\s*(\d+)'
                aave_match = re.search(aave_pattern, aave_part, re.IGNORECASE)
                if aave_match:
                    aave_scores[trait] = int(aave_match.group(1))

        if sae_start != -1:
            # Extract SAE scores
            sae_part = comparison[sae_start:]
            for trait in traits:
                sae_pattern = rf'{trait}:\s*(\d+)'
                sae_match = re.search(sae_pattern, sae_part, re.IGNORECASE)
                if sae_match:
                    sae_scores[trait] = int(sae_match.group(1))

        # If we found at least some scores, add the comparison to the results
        if any(aave_scores.values()) or any(sae_scores.values()):
            results.append((aave_scores, sae_scores))

    return results

def write_csv(results, output_file):
    traits = ['Intelligence', 'Kindness', 'Sophistication', 'Aggression', 'Emotional', 'Laziness', 'Factual']
    headers = ['AAVE_' + trait for trait in traits] + ['SAE_' + trait for trait in traits]

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        for aave, sae in results:
            row = {}
            for trait in traits:
                row['AAVE_' + trait] = aave.get(trait, '')
                row['SAE_' + trait] = sae.get(trait, '')
            writer.writerow(row)

# Usage
file_path = 'comparison_output.txt'
output_file = 'extracted_scores.csv'

results = extract_scores(file_path)
write_csv(results, output_file)

print(f"Extracted {len(results)} comparisons and saved to {output_file}")