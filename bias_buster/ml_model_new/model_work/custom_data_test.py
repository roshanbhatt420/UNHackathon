import pandas as pd 
from preprocessing_and_testing import make_custom_data

from scipy.stats import entropy




data = pd.read_csv("../data/heart.csv")
data=data.dropna()  # Drop rows with NaN values
custom_data= make_custom_data(data)
print(custom_data)


# Drop the 'Unnamed: 0' column if it exists
import joblib

# Load the model
model = joblib.load("../modelreport/sensitive_attribute_rf_model.joblib")


# Predict sensitivity (0 = not sensitive, 1 = sensitive)
predictions = model.predict(custom_data)

# feture namd and prediction
feature_names = data.columns.tolist()
sensitive_attribute=[]

for feature_name, prediction in zip(feature_names, predictions):
    sensitive_attribute.append(feature_name) if prediction == 1 else None


# calculation diffrent metrics for sensitive attribute
for feature_name in sensitive_attribute:
    def analyze_sensitive_column(data, column_name, target_column=None, positive_label=1):

      if column_name not in data.columns:
        raise ValueError(f"Column '{column_name}' not found in data.")

      sensitive_data = data[column_name]
      total_count = len(data)

      metrics = {}

    # Missing Value Ratio
      missing_ratio = sensitive_data.isnull().mean()
      metrics['missing_ratio'] = round(missing_ratio, 4)

    # Representation Proportions
      group_counts = sensitive_data.value_counts(normalize=True)
      metrics['representation_ratio'] = group_counts.to_dict()

    # Entropy of Sensitive Attribute
      group_probabilities = group_counts.values
      if len(group_probabilities) > 0:
        sensitive_entropy = entropy(group_probabilities, base=2)
      else:
        sensitive_entropy = 0.0
      metrics['entropy'] = round(sensitive_entropy, 4)

    # If target_column is given, calculate fairness-related metrics
      if target_column and target_column in data.columns:
        target_data = data[target_column]

        # Demographic Parity (Positive Outcome Rates)
        positive_rates = (
            data[data[target_column] == positive_label]
            [column_name]
            .value_counts(normalize=True)
        )
        metrics['positive_rate_per_group'] = positive_rates.to_dict()

        # Statistical Parity Difference (Max difference between groups)
        if len(positive_rates) >= 2:
            diff = positive_rates.max() - positive_rates.min()
            metrics['statistical_parity_difference'] = round(diff, 4)
        else:
            metrics['statistical_parity_difference'] = None

        # Disparate Impact
        if len(positive_rates) >= 2:
            groups = positive_rates.index.tolist()
            ratio = positive_rates.min() / positive_rates.max()
            metrics['disparate_impact'] = round(ratio, 4)
        else:
            metrics['disparate_impact'] = None
        
        # Group-wise Accuracy, Recall, Precision — you can expand here if you have prediction columns
      else:
        metrics['positive_rate_per_group'] = None
        metrics['statistical_parity_difference'] = None
        metrics['disparate_impact'] = None

      return metrics

    # Calculate entropy
    

# metrics accoding to sensitive attribute
    metrics = analyze_sensitive_column(data, feature_name, target_column='sesitivity')
    print(f"Metrics for {feature_name}:")
    for metric, value in metrics.items():
        print(f"{metric}: {value}")
    print("\n")