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
You are a professional data analyst.
Your task is to analyze the provided dataset carefully and generate a clear, complete, and professional conclusion.
In your conclusion, cover the following points:

- Summary: Describe the overall purpose and contents of the dataset (what it seems to represent).
- Data Quality: Comment on missing values, anomalies, duplicates, or noise.
- Distribution: Discuss the distribution of key features (especially any sensitive attributes if present).
- Potential Bias: Detect and explain any signs of bias, including underrepresentation, overrepresentation, or label imbalance.
- Important Patterns: Highlight important trends, relationships, or outliers discovered.
- Limitations: Identify any major limitations or risks in using this dataset for machine learning or decision-making.
- Suggestions: Give recommendations for improving dataset quality and fairness.

Important Notes:
- Be professional, objective, and concise.
- Use simple, understandable language, but keep it formal.
- If some information cannot be determined from the dataset, clearly state that.
- Do not hallucinate or assume anything not visible from the data.
- Give properly formated and styled markdown output with tables, lists, and headings.
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
    
