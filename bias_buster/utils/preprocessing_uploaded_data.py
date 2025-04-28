'''
This module contains functions to preprocess the uploaded data for bias detection.
'''
import pandas as pd

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
    






# function to check if the column has names
import spacy

# Load the small English model
nlp = spacy.load("en_core_web_sm")
def has_names(data, column_name):

    doc = nlp(data[column_name].astype(str).str.cat(sep=' '))  # Concatenate all values in the column into a single string
    for ent in doc.ents:
        if ent.label_ == "PERSON" or ent.label_=='GENDER' or ent.label_=='RACE' or ent.label_=="AGE":   # spaCy labels people as "PERSON"
            return "yes"
    return "no"



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
    custom_data['feature_name'] = data.columns
    custom_data['data_type'] = data.dtypes.values
    custom_data['has_names'] = [has_names(data, col) for col in data.columns]
    custom_data['unique_ratio'] = [calculate_unique_ratio(data, col) for col in data.columns]
    #use column names as semantic keywords
    custom_data['semantic_keywords'] = custom_data['feature_name']



    
    return custom_data





