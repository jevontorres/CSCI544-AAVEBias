import re
import pandas as pd
import os

def extract_all_traits_scores(prompt):
    """Extracts scores for all traits from a single prompt."""
    # List of traits to capture
    traits = ['Intelligence', 'Kindness', 'Sophistication', 'Aggression', 'Emotional', 'Laziness', 'Factual']

    # Find all occurrences of traits with scores
    matches = list(re.finditer(r'(Intelligence|Kindness|Sophistication|Aggression|Emotional|Laziness|Factual): (\d+\.?\d*)', prompt, re.IGNORECASE))

    # Split matches into AAVE and SAE sections based on occurrence order
    if len(matches) >= len(traits) * 2:  # Ensure enough matches for AAVE and SAE
        aave_scores = {f"AAVE {trait}": None for trait in traits}
        sae_scores = {f"SAE {trait}": None for trait in traits}

        for i, trait in enumerate(traits):
            aave_scores[f"AAVE {trait}"] = float(matches[i].group(2))  # First set of matches (AAVE)
            sae_scores[f"SAE {trait}"] = float(matches[i + len(traits)].group(2))  # Second set of matches (SAE)

        return {**aave_scores, **sae_scores}

    print(prompt)
    return None  # Return None if there are insufficient matches

def extract_paired_scores(text):
    """Extract scores for all prompts."""
    # Split the text into separate prompts
    prompts = text.split("Prompt")
    scores_data = []

    for prompt in prompts[1:]:  # Skip the first split which is not a prompt
        prompt_number_match = re.search(r"(\d+):", prompt)
        prompt_number = int(prompt_number_match.group(1)) if prompt_number_match else None

        # Extract AAVE and SAE scores for all traits
        scores = extract_all_traits_scores(prompt)

        if scores:
            row = {"Prompt": prompt_number, **scores}
            scores_data.append(row)

    return scores_data

def save_to_csv(scores_data, output_file):
    """Save extracted scores to a CSV file."""
    df = pd.DataFrame(scores_data)
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

def main():
    # Prompt the user for the input file name
    input_file = input("Please enter the name of the input file (e.g., 'aave_output_finetune.txt'): ").strip()

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()

        # Extract paired scores
        scores_data = extract_paired_scores(text)

        # Save to CSV
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}_paired_scores.csv"
        save_to_csv(scores_data, output_file)

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found. Please check the file name and try again.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the script
if __name__ == "__main__":
    main()