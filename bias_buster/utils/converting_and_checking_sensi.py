'''
checking data sensitivity and converting it to a format suitable for the model

'''
import pandas as pd
from preprocessing_uploaded_data import make_custom_data
import joblib

# # Load the model
# model = joblib.load("ml_model/modelreport/sensitive_attribute_rf_model.joblib")
# using garbage data for testing
data= pd.DataFrame({'name': ['John', 'Jane', 'Doe'],
                   'age': [28, 34, 45],
                   'Gender': ['male','male','female']})
# Convert the data to the custom format
custom_data = make_custom_data(data)
# Convert the DataFrame to a list of dictionaries
custom_data_list = custom_data.to_dict(orient='records')
print(custom_data_list)