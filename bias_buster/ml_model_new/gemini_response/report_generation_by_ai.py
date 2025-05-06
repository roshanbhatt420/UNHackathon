import pandas as pd
import google.generativeai as genai

def summarize_csv(file_path):
    # Load CSV
    df = pd.read_csv(file_path)

    # Create a simple description of the dataset
    summary = f"The dataset has {df.shape[0]} rows and {df.shape[1]} columns.\n\n"
    summary += "Columns and Data Types:\n"
    summary += df.dtypes.to_string()
    summary += "\n\nSample Data:\n"
    summary += df.head(5).to_string()
    return summary

def generate_conclusion(api_key, dataset_summary):
    # Configure Gemini client with API key
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-1.5-pro')  # You can also use gemini-1.5-flash or newer versions

    prompt = f"""
You are a professional data analyst with expertise in identifying patterns, assessing fairness, and evaluating data quality for machine learning and decision-making tasks.

Your task is to analyze the provided dataset and produce a structured, objective, and professional report. Your analysis should be thorough, unbiased, and based strictly on the data itself.

---

## Report Format

Follow this structure to write your report. Use clear markdown formatting with section headings, bullet points, and tables if necessary. Keep the tone formal, concise, and professional.

### 1. Summary

- Describe the overall purpose and context of the dataset.
- Identify what the dataset represents and its key contents (columns, rows, types).
- Mention the domain or problem area it relates to, if inferable.

### 2. Data Quality

- Report missing values, anomalies, duplicates, inconsistent formats, or outliers.
- Mention any signs of noise or data corruption.
- Use a table if needed to summarize issues by column.

### 3. Feature Distribution

- Analyze the distribution of important numerical and categorical features.
- Comment on skewness, sparsity, or imbalance.
- Highlight any sensitive attributes (e.g., gender, age, ethnicity), if available.

### 4. Potential Bias

- Detect signs of representation or sampling bias.
- Check for label imbalance or over/underrepresentation of specific groups.
- Note any areas where fairness might be a concern.

### 5. Important Patterns

- Highlight trends, correlations, or unexpected relationships.
- Mention any segments of interest or outliers that may require deeper inspection.
- Use concise descriptions or tables to summarize key insights.

### 6. Limitations

- Identify major limitations for using this dataset in analysis or machine learning.
- Mention issues like data drift, missing contextual features, or unclear labels.

### 7. Recommendations

- Suggest improvements for data collection, labeling, or preprocessing.
- Recommend specific steps to improve quality, fairness, or model-readiness.
- Be practical and actionable in your suggestions.

---

## Additional Guidelines

- Be objective. Do not guess or hallucinate missing context.
- If something cannot be assessed from the data, explicitly state that.
- Use proper markdown formatting for clarity (e.g., lists, tables, headings).
- Avoid unnecessary technical jargon; keep the language accessible but professional.

---


{dataset_summary}

"""

    # Generate response
    response = model.generate_content(prompt)
    print(response.text)


    return response.text



def do_response(csv_file_path):
    # === 🔥 SET THESE ===   
    api_key = "AIzaSyD0NwDy0GYqlBR2jK2SlyzdN9BeQWmMmrs"           # Your Gemini API Key      # Your CSV file path

    dataset_summary = summarize_csv(csv_file_path)
    summary=generate_conclusion(api_key, dataset_summary)
    return summary
    
