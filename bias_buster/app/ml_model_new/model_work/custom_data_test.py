import pandas as pd 
# importing make_custom_data function from preprocessing_and_testing.py

from scipy.stats import entropy
import joblib
from preprocessing_and_testing import make_custom_data
csv_file_path = "../data/heart.csv"  # Path to your CSV file
def process_csv_with_model(csv_file_path):
  data = pd.read_csv(csv_file_path)
  data = data.dropna()  # Drop rows with NaN values
  custom_data = make_custom_data(data)

  # Load the model
  model = joblib.load("../modelreport/sensitive_attribute_rf_model.joblib")

  # Predict sensitivity (0 = not sensitive, 1 = sensitive)
  predictions = model.predict(custom_data)

  # Feature names and predictions
  feature_names = data.columns.tolist()
  sensitive_attribute = []

  for feature_name, prediction in zip(feature_names, predictions):
    if prediction == 1:
      sensitive_attribute.append(feature_name)

  # Function to calculate metrics for a sensitive column
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
        ratio = positive_rates.min() / positive_rates.max()
        metrics['disparate_impact'] = round(ratio, 4)
      else:
        metrics['disparate_impact'] = None
    else:
      metrics['positive_rate_per_group'] = None
      metrics['statistical_parity_difference'] = None
      metrics['disparate_impact'] = None

    return metrics

  # Collect metrics for all sensitive attributes
  all_metrics = {}
  for feature_name in sensitive_attribute:
    metrics = analyze_sensitive_column(data, feature_name, target_column='sesitivity')
    all_metrics[feature_name] = metrics

  return all_metrics

print(process_csv_with_model(csv_file_path))
