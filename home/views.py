# home/views.py
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


# def about(request):
#     return render(request, 'home/about.html')
# def contact(request):
#     return render(request, 'home/contact.html')
# def terms(request):
#     return render(request, 'home/terms.html')
# def privacy(request):
#     return render(request, 'home/privacy.html')
# def faq(request):
#     return render(request, 'home/faq.html')
# def pricing(request):
#     return render(request, 'home/pricing.html')
# def features(request):
#     return render(request, 'home/features.html')
# def dashboard(request):
#     return render(request, 'home/dashboard.html')
def home_index(request):
    return render(request, 'index.html')
