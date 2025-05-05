from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from utils.preprocessing_uploaded_data import make_custom_data
import joblib

# Load the pre-trained model
MODEL_PATH = 'ml_model_new/modelreport/sensitive_attribute_rf_model.joblib'
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
def check_page(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        # Get the uploaded file
        csv_file = request.FILES['csv_file']
        
        processed_data = process_csv_with_model(csv_file)
        
        # Summarize the processed data
        summary = summarize_csv(csv_file)
        
        # Return the summary as JSON response
        return JsonResponse({'result': summary})
    
    # Render the check.html template for GET requests
    return render(request, 'check.html')
