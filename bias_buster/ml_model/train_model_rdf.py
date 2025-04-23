import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer

def train_classifier():
    # Reading data
    data = pd.read_csv("data/metadata.csv")
    # One-hot encode categorical columns
    df_encoded = pd.get_dummies(data, columns=['data_type', 'has_names'])

    # Drop unused or problematic columns
    columns_to_drop = ['likely_values']
    df_cleaned = df_encoded.drop(columns=columns_to_drop)

    # Separate features and targetfjfff
    x = df_cleaned.drop(columns=['is_sensitive'])
    y = df_cleaned['is_sensitive'] 


    preprocessor = preprocess_data()
    X_transformed = preprocessor.fit_transform(x)


    # Splitting the data into training and testing sets
    xtrain, xtest, ytrain, ytest = train_test_split(X_transformed, y, test_size=0.2, random_state=42)
    

    # Training the Random Forest model
    rmf = RandomForestClassifier(random_state=42)
    rmf.fit(xtrain, ytrain)

    # Making predictions
    model_predictions = rmf.predict(xtest)
    print(model_predictions)


    # Generating and saving classification report
    report = classification_report(ytest, model_predictions)
    print(report)
    with open("class_report.txt", "w") as f:
        f.write(report)

    # Saving feature importance
    # feature_importance = pd.DataFrame({'features': X_transformed.columns, 'importance': rmf.feature_importances_}).sort_values('importance', ascending=False)
    # print("Feature importance is added")
    # feature_importance.to_csv("feature.csv", index=False)

    # Generating and saving confusion matrix
    plt.figure(figsize=(8, 6))
    matrix = confusion_matrix(ytest, model_predictions)
    sns.heatmap(matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['no_sensitive', 'sensitive'], yticklabels=['no_sensitive', 'sensitive'])
    plt.title("Confusion Matrix:")
    plt.ylabel("True Label")
    plt.xlabel("Predicted Label")

    # Saving the confusion matrix plot
    plt.savefig("confusion_matrix.png")
    plt.show()
    return rmf


  # Build ColumnTransformer
def preprocess_data():
    preprocessor = ColumnTransformer(
        transformers=[
            ('tfidf_keywords', TfidfVectorizer(stop_words='english', max_features=100), 'semantic_keywords'),
            ('tfidf_feature_name', TfidfVectorizer(stop_words='english', max_features=100), 'feature_name'),
            ('scale_ratio', StandardScaler(), ['unique_ratio']),
        ],
        remainder='passthrough'
    )
    return preprocessor
    



