import sys
import pandas as pd
import google.generativeai as genai
import openpyxl
import numpy as np
import re

from scipy import stats

import pandas as pd
from scipy import stats
import numpy as np

# File paths
sae_file_path = '/Users/kritee/Documents/CSCI544/sae_individual_res.xlsx'
aave_file_path = '/Users/kritee/Documents/CSCI544/aave_individual_result.xlsx'

# Specify the trait columns
trait_columns = ["Intelligence", "Kindness", "Sophistication", "Aggression", "Emotional", "Laziness", "Factual"]

# Load SAE and AAVE data
SAEdata = pd.read_excel(sae_file_path, usecols=trait_columns)
AAVEdata = pd.read_excel(aave_file_path, usecols=trait_columns)

# Convert non-numeric values to NaN
SAEdata = SAEdata.apply(pd.to_numeric, errors='coerce')
AAVEdata = AAVEdata.apply(pd.to_numeric, errors='coerce')

# Function to calculate Cohen's d
def calculate_cohens_d(mean1, mean2, sd1, sd2):
    pooled_std = np.sqrt((sd1**2 + sd2**2) / 2)
    return (mean2 - mean1) / pooled_std if pooled_std != 0 else 0.0

# List to store results
results = []

for trait in trait_columns:
    # Drop NaN values for the current trait
    sae_values = SAEdata[trait].dropna()
    aave_values = AAVEdata[trait].dropna()

    # Check if there is enough data to perform calculations
    if len(sae_values) > 1 and len(aave_values) > 1:
        # Perform T-Test
        t_stat, p_value = stats.ttest_ind(sae_values, aave_values, equal_var=False)
        
        # Calculate means and standard deviations
        mean_sae = sae_values.mean()
        std_sae = sae_values.std(ddof=1)
        mean_aave = aave_values.mean()
        std_aave = aave_values.std(ddof=1)
        
        # Calculate Cohen's d
        cohens_d = calculate_cohens_d(mean_sae, mean_aave, std_sae, std_aave)
        
        # Calculate percentage difference
        percentage_diff = abs(mean_sae - mean_aave) / mean_sae * 100 if mean_sae != 0 else 0
        
        # Determine significance
        significance = "Significant" if p_value < 0.05 else "Not Significant"
        
        # Append results
        results.append([
            trait,
            round(mean_sae, 4),
            round(std_sae, 4),
            round(mean_aave, 4),
            round(std_aave, 4),
            round(t_stat, 4),
            round(p_value, 4),
            round(cohens_d, 4),
            round(percentage_diff, 2),
            significance
        ])

# Create a consolidated DataFrame for all results
results_df = pd.DataFrame(
    results,
    columns=[
        "Trait", "Mean_SAE", "Std_SAE", "Mean_AAVE", "Std_AAVE",
        "T-Statistic", "P-Value", "Cohen's d", "Percentage Difference", "Significance"
    ]
)

# Save the consolidated table to Excel
consolidated_file_path = '/Users/kritee/Documents/CSCI544/results_comp_ind.xlsx'
results_df.to_excel(consolidated_file_path, index=False)

# Print the consolidated table to the debug console
pd.set_option('display.float_format', '{:.4f}'.format)  # Format for cleaner console output
print("\nConsolidated Results:")
print(results_df.to_string(index=False))

# Save to CSV (optional)
results_df.to_csv('/Users/kritee/Documents/CSCI544/results_comp_ind.csv', index=False)

print(f"\nT-Test results with Cohen's d saved to {consolidated_file_path}")
