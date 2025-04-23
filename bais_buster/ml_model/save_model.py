import joblib
import pandas as  pd
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from train_model_rdf import train_classifier  # adjust the import path if needed
# importing preprocessor from the training script
from train_model_rdf import preprocess_data  # adjust the import path if needed
  # adjust the import path if needed


# Train the model
# model = train_classifier()


def preprocess_custom_data(raw_data: pd.DataFrame, required_columns: list) -> pd.DataFrame:
   
    # Apply the same one-hot encoding
    data_encoded = pd.get_dummies(raw_data, columns=['data_type', 'has_names'])

    # Drop columns not used in model
    if 'likely_values' in data_encoded.columns:
        data_encoded = data_encoded.drop(columns=['likely_values'])

    # Add any missing one-hot columns (set to 0)
    for col in required_columns:
        if col not in data_encoded.columns:
            data_encoded[col] = 0

    # Ensure correct column order
    data_encoded = data_encoded[required_columns]

    # Transform with preprocessor
    x_custom_data=preprocess_data(data_encoded)
    return x_custom_data
    

custom_data = pd.DataFrame([{
    'feature_name': 'user_email',
    'semantic_keywords': 'email, contact, address',
    'unique_ratio': 0.95,
    'data_type': 'string',
    'has_names': 'yes'
}])

preprocessor = preprocess_data()
x_custom_data = preprocessor.fit_transform(custom_data)


# loading preprocessor from the training script




model= train_classifier()

# Make predictions on the custom data
print("Transformed custom data:")
print("")
predictions = model.predict(x_custom_data)
print(predictions)



# Save the model
