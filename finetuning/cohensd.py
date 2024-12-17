import pandas as pd
import numpy as np

def calculate_cohens_d(mean1, std1, n1, mean2, std2, n2):
    """Calculate Cohen's d for two groups."""
    pooled_std = np.sqrt(((n1 - 1) * std1**2 + (n2 - 1) * std2**2) / (n1 + n2 - 2))
    return (mean1 - mean2) / pooled_std

def main(csv1, csv2, output_csv):
    # Load the CSV files, specifying no header for the first column
    df1 = pd.read_csv(csv1, names=["Variable", "Mean", "Std", "t_statistic", "p_value"], skiprows=1)
    df2 = pd.read_csv(csv2, names=["Variable", "Mean", "Std", "t_statistic", "p_value"], skiprows=1)

    # Assume equal sample sizes for both groups (adjust as necessary)
    n1 = n2 = 261  # Replace with actual sample sizes if known

    # Merge the two dataframes
    merged = pd.merge(df1, df2, on="Variable", suffixes=('_group1', '_group2'))

    # Calculate Cohen's d for each variable
    cohens_d_results = []
    for _, row in merged.iterrows():
        d = calculate_cohens_d(
            row['Mean_group1'], row['Std_group1'], n1,
            row['Mean_group2'], row['Std_group2'], n2
        )
        cohens_d_results.append({'Variable': row['Variable'], 'Cohen_d': d})

    # Create a DataFrame with the results
    cohens_d_df = pd.DataFrame(cohens_d_results)

    # Save the results to a CSV
    cohens_d_df.to_csv(output_csv, index=False)
    print(f"Cohen's d values saved to {output_csv}")

if __name__ == "__main__":
    # Example usage
    csv1 = "sae_output_finetune_statistics.csv"  # Replace with the path to the first CSV
    csv2 = "aave_output_finetune_statistics.csv"  # Replace with the path to the second CSV
    output_csv = "cohens_d_results.csv"  # Replace with the desired output path

    main(csv1, csv2, output_csv)