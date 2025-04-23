import pandas as pd
from scipy.stats import chi2_contingency, ks_2samp
from scipy.stats import power_divergence

'''
Functionality: Performs statistical analysis on the column data to identify potential biasness.

Input: CSV file Column data for testing biasness.

Output: A dictionary containing the results of the biasness analysis.
'''

def check_attribute_biasness(column_data):
    """
    Performs statistical analysis on the column data to identify potential biasness.

    Parameters:
        column_data (pd.Series): A pandas Series containing the column data for testing biasness.

    Returns:
        dict: A dictionary containing the results of the biasness analysis.
    """
    if not isinstance(column_data, pd.Series):
        raise ValueError("Input data must be a pandas Series.")

    # Count the occurrences of each unique value in the column
    value_counts = column_data.value_counts()

    # Create a contingency table
    contingency_table = pd.DataFrame({'Observed': value_counts})

    # Perform the Chi-Square test
    chi2, p_value_chi2, _, _ = chi2_contingency([contingency_table['Observed']])

    # Perform the G-test (likelihood ratio test)
    g_stat, p_value_g_test = power_divergence(f_obs=contingency_table['Observed'], lambda_="log-likelihood")

    # Perform the Kolmogorov-Smirnov test (against uniform distribution)
    uniform_dist = pd.Series([1 / len(value_counts)] * len(value_counts), index=value_counts.index)
    ks_stat, p_value_ks = ks_2samp(value_counts, uniform_dist * sum(value_counts))

    # Determine if bias is present based on p-values
    is_biased_chi2 = p_value_chi2 < 0.05
    is_biased_g_test = p_value_g_test < 0.05
    is_biased_ks = p_value_ks < 0.05

    return {
        "chi2_test": {
            "chi2_statistic": chi2,
            "p_value": p_value_chi2,
            "is_biased": is_biased_chi2
        },
        "g_test": {
            "g_statistic": g_stat,
            "p_value": p_value_g_test,
            "is_biased": is_biased_g_test
        },
        "ks_test": {
            "ks_statistic": ks_stat,
            "p_value": p_value_ks,
            "is_biased": is_biased_ks
        },
        "value_counts": value_counts.to_dict()
    }
