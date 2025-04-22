import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

def train_classifier():
    # Reading data
    data = pd.read_csv("data/data.csv")
    data = data.drop(columns=['feature_name', 'likely_values'])

    # converting has_name to 1 and 0\
    data['has_names'] = data['has_names'].map({'yes': 1, 'no': 0})
    

    # data encodeing 

    le_data_type = LabelEncoder()
    data['data_type'] = le_data_type.fit_transform(data['data_type'])


    le_keywords = LabelEncoder()
    data['semantic_keywords'] = le_keywords.fit_transform(data['semantic_keywords'])



    
    # Splitting data into features and target
    x = data.drop("is_sensitive", axis=1)
    y = data["is_sensitive"]

    # Splitting the data into training and testing sets
    xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=42)

    # Training the Random Forest model
    rmf = RandomForestClassifier(random_state=42)
    rmf.fit(xtrain, ytrain)

    # Making predictions
    model_predictions = rmf.predict(xtest)

    # Generating and saving classification report
    report = classification_report(ytest, model_predictions)
    print(report)
    with open("class_report.txt", "w") as f:
        f.write(report)

    # Saving feature importance
    feature_importance = pd.DataFrame({'features': x.columns, 'importance': rmf.feature_importances_}).sort_values('importance', ascending=False)
    print("Feature importance is added")
    feature_importance.to_csv("feature.csv", index=False)

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

train_classifier()
