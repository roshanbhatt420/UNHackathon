import pandas as pd 
# importing make_custom_data function from preprocessing_and_testing.py

from scipy.stats import entropy
import joblib
from .preprocessing_and_testing import make_custom_data
# csv_file_path = "../data/heart.csv"  # Path to your CSV file
def process_csv_with_model(csv_file_path):
  """
  Process the CSV file and return the model's response.
  """
  try:
    # Check if the file is a valid CSV
    if csv_file_path.size == 0:
      raise ValueError("The uploaded file is empty. Please upload a valid CSV file.")

    # Attempt to read the CSV file
    data = pd.read_csv(csv_file_path)
    if data.empty:
      raise ValueError("The uploaded CSV file contains no data.")

    print(f"Reading CSV file from: {csv_file_path}")
    print(f"Initial data shape: {data.shape}")
    
    data = data.dropna()  # Drop rows with NaN values
    print(f"Data shape after dropping NaN values: {data.shape}")
    
    custom_data = make_custom_data(data)
    print(f"Custom data shape: {custom_data.shape}")

    # Load the model
    print("Loading the model...")
    model = joblib.load("ml_model_new/modelreport/sensitive_attribute_rf_model.joblib")
    print("Model loaded successfully.")

    # Predict sensitivity (0 = not sensitive, 1 = sensitive)
    print("Making predictions...")
    predictions = model.predict(custom_data)
    print(f"Predictions: {predictions}")

    # Feature names and predictions
    feature_names = data.columns.tolist()
    print(f"Feature names: {feature_names}")
    
    sensitive_attribute = []

    for feature_name, prediction in zip(feature_names, predictions):
      if prediction == 1:
        sensitive_attribute.append(feature_name)
    print(f"Sensitive attributes identified: {sensitive_attribute}")

    # Function to calculate metrics for a sensitive column
    def analyze_sensitive_column(data, column_name, target_column=None, positive_label=1):
      print(f"Analyzing sensitive column: {column_name}")
      if column_name not in data.columns:
        raise ValueError(f"Column '{column_name}' not found in data.")

      sensitive_data = data[column_name]
      total_count = len(data)

      metrics = {}

      # Missing Value Ratio
      missing_ratio = sensitive_data.isnull().mean()
      metrics['missing_ratio'] = round(missing_ratio, 4)
      print(f"Missing ratio for {column_name}: {metrics['missing_ratio']}")

      # Representation Proportions
      group_counts = sensitive_data.value_counts(normalize=True)
      metrics['representation_ratio'] = group_counts.to_dict()
      print(f"Representation ratio for {column_name}: {metrics['representation_ratio']}")

      # Entropy of Sensitive Attribute
      group_probabilities = group_counts.values
      if len(group_probabilities) > 0:
        sensitive_entropy = entropy(group_probabilities, base=2)
      else:
        sensitive_entropy = 0.0
      metrics['entropy'] = round(sensitive_entropy, 4)
      print(f"Entropy for {column_name}: {metrics['entropy']}")

      # If target_column is given, calculate fairness-related metrics
      if target_column and target_column in data.columns:
        target_data = data[target_column]
        print(f"Target column '{target_column}' found. Calculating fairness metrics...")

        # Demographic Parity (Positive Outcome Rates)
        positive_rates = (
          data[data[target_column] == positive_label]
          [column_name]
          .value_counts(normalize=True)
        )
        metrics['positive_rate_per_group'] = positive_rates.to_dict()
        print(f"Positive rate per group for {column_name}: {metrics['positive_rate_per_group']}")

        # Statistical Parity Difference (Max difference between groups)
        if len(positive_rates) >= 2:
          diff = positive_rates.max() - positive_rates.min()
          metrics['statistical_parity_difference'] = round(diff, 4)
        else:
          metrics['statistical_parity_difference'] = None
        print(f"Statistical parity difference for {column_name}: {metrics['statistical_parity_difference']}")

        # Disparate Impact
        if len(positive_rates) >= 2:
          ratio = positive_rates.min() / positive_rates.max()
          metrics['disparate_impact'] = round(ratio, 4)
        else:
          metrics['disparate_impact'] = None
        print(f"Disparate impact for {column_name}: {metrics['disparate_impact']}")
      else:
        metrics['positive_rate_per_group'] = None
        metrics['statistical_parity_difference'] = None
        metrics['disparate_impact'] = None
        print(f"No target column provided or not found for {column_name}. Skipping fairness metrics.")

      return metrics

    # Collect metrics for all sensitive attributes
    all_metrics = {}
    for feature_name in sensitive_attribute:
      print(f"Collecting metrics for sensitive attribute: {feature_name}")
      metrics = analyze_sensitive_column(data, feature_name, target_column='sesitivity')
      all_metrics[feature_name] = metrics

    print("All metrics collected.")
    return all_metrics
  except pd.errors.EmptyDataError:
    raise ValueError("The uploaded file is not a valid CSV or is empty.")
  except Exception as e:
    raise Exception(f"Error processing the CSV file: {str(e)}")
