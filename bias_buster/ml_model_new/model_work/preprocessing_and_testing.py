'''
This module contains functions to preprocess the uploaded data for bias detection.
'''
import pandas as pd
import numpy as np


# function to calculate missing ratio

def calculate_missing_ratio_for_column(df, column_name):
    """
    Calculate the missing ratio for a specific column.

    Args:
        df (pandas.DataFrame): The input dataset.
        column_name (str): The column for which to calculate the missing ratio.

    Returns:
        float: Missing ratio (between 0 and 1) for the specified column.
    """
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame.")

    missing_ratio = df[column_name].isnull().mean()
    return missing_ratio

# function to check if the column has sensitive keywords
import pandas as pd

def has_sensitive_keywords(data, column_name):
    """
    Check if a column name contains sensitive keywords.

    Args:
        data (pandas.DataFrame): The input dataset.
        column_name (str): The column name to check for sensitive keywords.

    Returns:
        int: 1 if sensitive keyword is found in the column name, 0 otherwise.
    """
    sensitive_keywords = {
        "age", "gender", "sex", "race", "ethnicity", "income", "salary",
        "email", "phone", "address", "ssn", "religion", "marital",
        "birth", "nationality", "citizenship"
    }

    if column_name not in data.columns:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame.")

    # Check if any sensitive keyword is a substring of the column name (case-insensitive)
    column_name_lower = column_name.lower()
    for keyword in sensitive_keywords:
        if keyword in column_name_lower:
            return 1  # Sensitive
    return 0  # Not sensitive



# function to calculate entropy
def calculate_entropy_for_column(df, column_name):
    """
    Calculate the entropy of a specific column.

    Args:
        df (pandas.DataFrame): Input dataset.
        column_name (str): The column for which to calculate entropy.

    Returns:
        float: Entropy value.
    """
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame.")

    # Get the value counts (probability distribution)
    value_counts = df[column_name].value_counts(normalize=True, dropna=True)

    # Calculate entropy
    entropy = -np.sum(value_counts * np.log2(value_counts))

    return entropy



# function to calcualte unique ratio
def calculate_unique_ratio(data,column_name):
    """unique ration =(number of unique values)/(total number of values)"""

    # Check if the column exists in the DataFrame
    if column_name not in data.columns:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame.")
    unique_count = data[column_name].nunique()
    total_count = data[column_name].count()
    # return zero to avoid division by zero
    if total_count == 0:
        return 0
    else:
        return unique_count / total_count 
    

#making custom data
"""
function to make custom data for bias detection
    input: dataframe
    output: dataframe with columns ['feature_name', 'data_type', 'has_names', 'unique_ratio', 'semantic_keywords']
"""
def make_custom_data(data):
    """
    Function to create custom data for bias detection.
    
    Parameters:
        data (pd.DataFrame): The input DataFrame containing the data.
        
    Returns:
        pd.DataFrame: A DataFrame with the columns ['feature_name', 'data_type', 'has_names', 'unique_ratio', 'semantic_keywords'].
    """
    custom_data = pd.DataFrame()
    custom_data['column_name'] = data.columns
    # checking data type(string ,int,float,bool)
    custom_data['data_type'] = [str(data[col].dtype) for col in data.columns]
    custom_data['unique_ratio'] = [calculate_unique_ratio(data, col) for col in data.columns]
    #use column names as semantic keywords
    custom_data['missing_ratio'] = [calculate_missing_ratio_for_column(data, col) for col in data.columns]
    custom_data['has_sensitive_keyword'] = [has_sensitive_keywords(data, col) for col in data.columns]
    custom_data['entropy'] = [calculate_entropy_for_column(data, col) for col in data.columns]
    return custom_data






