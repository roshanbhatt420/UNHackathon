from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import markdown
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
    # Handle uploaded CSV file
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        print(f"Received file: {uploaded_file.name}, size: {uploaded_file.size}")
        # Check if the uploaded file is empty
        if uploaded_file.size == 0:
            print("Uploaded file is empty.")
            return render(request, 'check.html', {'error': 'The uploaded file is empty. Please upload a valid CSV file.'})
        try:
            # Process the uploaded file
            print("Processing uploaded file...")
            result = process_uploaded_file(uploaded_file)
            print("File processed successfully.")
            return render(request, 'check.html', result)
        except Exception as e:
            print(f"Error during file processing: {str(e)}")
            return render(request, 'check.html', {'error': f'An error occurred while processing the file: {str(e)}'})
    # Render the check.html template for GET requests
    print("Rendering check.html for GET request.")
    return render(request, 'check.html')


def process_uploaded_file(uploaded_file):
    """
    Process the uploaded file using the gemini model and custom data processing.
    Returns a dictionary with the results or error messages.
    """
    try:
        # Process the file content with do_response
        summary = do_response(uploaded_file)
        result = markdown.markdown(summary, extensions=['fenced_code', 'tables', 'codehilite', 'toc'])

        # Rewind the file pointer and process with process_csv_with_model
        uploaded_file.seek(0)
        model_response = process_csv_with_model(uploaded_file)
        print("Model response:", model_response)
        return {'result_model': model_response, 'result':result}
    except Exception as e:
        raise Exception(f"Error during file processing: {str(e)}")
