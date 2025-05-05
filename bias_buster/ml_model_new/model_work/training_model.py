import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

# Ensure output directories exist
os.makedirs("modelreport", exist_ok=True)

# Reading the data
df= pd.read_csv("data/data.csv")
df=df.drop(columns=['avg_str_len'])



# Separate features and target
x = df.drop(columns=['sesitivity'])
y = df['sesitivity']

# Define categorical and numerical features
categorical_features = ['column_name', 'data_type']
numeric_features = ['unique_ratio','missing_ratio','has_sensitive_keyword','entropy']

# Preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        ('num', 'passthrough', numeric_features)
    ]
)

# Full pipeline: preprocessing + classifier
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

# Train-test split
xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=42)

# Train the model
model_pipeline.fit(xtrain, ytrain)

# Predict on test set
ypred = model_pipeline.predict(xtest)
# Classification report
report = classification_report(ytest, ypred, target_names=['no_sensitive', 'sensitive'], output_dict=True)

with open("modelreport/class_report.txt", "w") as f:
    json.dump(report, f)

# # Confusion matrix
# cm = confusion_matrix(ytest, ypred)
# cm_df = pd.DataFrame(cm, index=['no_sensitive', 'sensitive'], columns=['no_sensitive', 'sensitive'])
# plt.figure(figsize=(10, 7))
# sns.heatmap(cm_df, annot=True, fmt='d', cmap='Blues')
# plt.title('Confusion Matrix')
# plt.savefig("modelreport/confusion_matrix.png")
# plt.show()

import os
# import pickle

# # Ensure the directory exists
# os.makedirs("modelreport", exist_ok=True)

# # Define the model path
# model_path = "modelreport/sensitive_attribute_rf_model.joblib"
# # print(f"Model path: {model_path}")
# # dumping model with joblib
# joblib.dump(model_pipeline, model_path)
# print(f"Model saved to {model_path}")   
