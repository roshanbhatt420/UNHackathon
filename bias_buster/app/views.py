from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from utils.preprocessing_uploaded_data import make_custom_data
import joblib

# Load the pre-trained model
MODEL_PATH = 'bias_buster/ml_model/modelreport/sensitive_attribute_rf_model.joblib'
model = joblib.load(MODEL_PATH)

# Create your views here.

def home_page(request):
    # Render the index.html template
    return render(request, 'index.html')


def about_page(request):
    # Render the about.html template
    return render(request, 'about.html')


def project_page(request):
    # Render the project.html template
    return render(request, 'project.html')


@csrf_exempt
def upload_and_analyze(request):
    if request.method == 'POST':
        # Parse uploaded CSV file
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        try:
            # Read the CSV file into a DataFrame
            data = pd.read_csv(uploaded_file)

            # Preprocess the data
            custom_data = make_custom_data(data)

            # Perform predictions using the model
            predictions = model.predict(custom_data)

            # Return predictions as JSON
            return JsonResponse({'predictions': predictions.tolist()})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
