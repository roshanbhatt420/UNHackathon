from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
# fetching gemini model from the ml_model_new directory
from ml_model_new.gemini_response.report_generation_by_ai import do_response

# importing make_custom_data function from preprocessing_and_testing.py
from ml_model_new.model_work.custom_data_test import process_csv_with_model

def home_page(request):
    # Render the index.html template
    return render(request, 'index.html')


def about_page(request):
    # Render the about.html template
    return render(request, 'about.html')




@csrf_exempt
def check_page(request):
    # handle uploaded csv file 
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']

        # Check if the uploaded file is empty
        if uploaded_file.size == 0:
            return render(request, 'check.html', { 'error': 'The uploaded file is empty. Please upload a valid CSV file.' })

        try:
            # sending file to the gemini model for processing
            summary = do_response(uploaded_file)
            model_response = process_csv_with_model(uploaded_file)
            return render(request, 'check.html', { 'result_model': model_response, 'result': summary })
        except Exception as e:
            return render(request, 'check.html', { 'error': f'An error occurred while processing the file: {str(e)}' })

    # Render the check.html template for GET requests
    return render(request, 'check.html')
