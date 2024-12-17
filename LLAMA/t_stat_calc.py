import pandas as pd
import numpy as np
from scipy import stats

def calculate_statistics(sae_file, aave_file):
    # Read CSV files
    sae_df = pd.read_csv(sae_file, index_col=0)
    aave_df = pd.read_csv(aave_file, index_col=0)
    
    # Hardcode sample sizes
    n1 = 2019-716  # SAE
    n2 = 2019-754  # AAVe
    
    def calculate_t_stat(means1, stds1, n1, means2, stds2, n2):
        """Calculate t-statistic for each trait"""
        return (means1 - means2) / np.sqrt((stds1**2/n1) + (stds2**2/n2))
    
    def calculate_cohens_d(means1, stds1, means2, stds2):
        """Calculate Cohen's d effect size"""
        pooled_std = np.sqrt((stds1**2 + stds2**2) / 2)
        return (means1 - means2) / pooled_std
    
    def interpret_cohens_d(d):
        if abs(d) < 0.2:
            return 'Negligible'
        elif abs(d) < 0.5:
            return 'Small'
        elif abs(d) < 0.8:
            return 'Medium'
        else:
            return 'Large'
    
    def calculate_p_value(t_stats, df1, df2):
        """Calculate two-tailed p-value"""
        df_combined = df1 + df2 - 2
        return stats.t.sf(np.abs(t_stats), df_combined) * 2
    
    # Calculate statistics
    t_stats = calculate_t_stat(
        sae_df['mean'], 
        sae_df['std'], 
        n1,
        aave_df['mean'], 
        aave_df['std'], 
        n2
    )
    
    cohens_d = calculate_cohens_d(
        sae_df['mean'],
        sae_df['std'],
        aave_df['mean'],
        aave_df['std']
    )
    
    p_values = calculate_p_value(t_stats, n1, n2)
    
    # Create results DataFrame
    results = pd.DataFrame({
        'mean_sae': sae_df['mean'].round(8),
        'std_sae': sae_df['std'].round(8),
        'mean_aave': aave_df['mean'].round(8),
        'std_aave': aave_df['std'].round(8),
        't_statistic': t_stats.round(8),
        'p_value': p_values.round(8),
        'cohens_d': cohens_d.round(8),
        'p_value_significance': ['Significant' if p < 0.05 else 'Not Significant' for p in p_values],
        'cohens_d_interpretation': [interpret_cohens_d(d) for d in cohens_d]
    })
    
    return results

if __name__ == "__main__":
    sae_file = "sae_score_statistics_6.csv"
    aave_file = "aave_score_statistics_6.csv"
    
    results = calculate_statistics(sae_file, aave_file)
    print("\nStatistical Analysis Results:")
    print(results)
    
    results.to_csv("okfile.csv")