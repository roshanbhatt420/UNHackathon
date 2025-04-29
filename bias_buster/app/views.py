from django.shortcuts import render


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
