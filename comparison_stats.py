import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

def calculate_cohen_d(a, b):
    """Calculate Cohen's d effect size."""
    pooled_std = np.sqrt(((len(a) - 1) * np.std(a) ** 2 + (len(b) - 1) * np.std(b) ** 2) / (len(a) + len(b) - 2))
    if pooled_std == 0:
        return 0
    else:
        return (np.mean(a) - np.mean(b)) / pooled_std

def interpret_cohens_d(cohens_d):
    """Interpret Cohen's d effect size."""
    abs_d = abs(cohens_d)
    if abs_d < 0.2:
        return 'Negligible'
    elif abs_d < 0.5:
        return 'Small'
    elif abs_d < 0.8:
        return 'Medium'
    else:
        return 'Large'

def calculate_statistics(file_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    # Replace empty values with 0
    df = df.fillna(0)
    # Calculate the averages, standard deviations, and Cohen's d for each trait
    trait_stats = []
    for trait in ['Intelligence', 'Kindness', 'Sophistication', 'Aggression', 'Emotional', 'Laziness', 'Factual']:
        aave_scores = df[f'AAVE_{trait}'].astype(float)
        sae_scores = df[f'SAE_{trait}'].astype(float)
        aave_mean = round(aave_scores.mean(), 8)
        aave_std = round(aave_scores.std(), 8)
        sae_mean = round(sae_scores.mean(), 8)
        sae_std = round(sae_scores.std(), 8)
        t_stat, p_value = ttest_ind(aave_scores, sae_scores)
        cohens_d = round(calculate_cohen_d(aave_scores, sae_scores), 8)
        cohens_d_interpretation = interpret_cohens_d(cohens_d)
        trait_stats.append({
            'Trait': trait,
            'AAVE_Mean': aave_mean,
            'AAVE_Std': aave_std,
            'AAVE_Count': len(aave_scores),
            'SAE_Mean': sae_mean,
            'SAE_Std': sae_std,
            'SAE_Count': len(sae_scores),
            't_Stat': round(t_stat, 8),
            'p_Value': round(p_value, 8),
            'Cohen_d': cohens_d,
            'Cohen_d_Interpretation': cohens_d_interpretation
        })
    return trait_stats

def write_csv(results, output_file):
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)

# Usage
file_path = 'extracted_scores.csv'
output_file = 'comparison_statistics_finals.csv'
trait_statistics = calculate_statistics(file_path)
write_csv(trait_statistics, output_file)
print(f"Calculated statistics saved to {output_file}")