import pandas as pd
import joblib

# Load the model
model = joblib.load("modelreport/sensitive_attribute_rf_model.joblib")

# Define custom data (must match training format, excluding 'likely_values' and 'is_sensitive')
custom_data = pd.DataFrame([
    {
        "feature_name": "phome_number",
        "data_type": "string",
        "has_names": "yes",
        "unique_ratio": 0.9,
        "semantic_keywords": "contact,phone"
    },
    {
        "feature_name": "height",
        "data_type": "float",
        "has_names": "no",
        "unique_ratio": 0.4,
        "semantic_keywords": "body,measurement"
    }
])

# Predict sensitivity (0 = not sensitive, 1 = sensitive)
predictions = model.predict(custom_data)

# Output predictions
for i, pred in enumerate(predictions):
    label = "Sensitive" if pred == 1 else "Not Sensitive"
    print(f"Attribute {i+1}: {label}")
