# Mediap/root_urls.py
from django.urls import path, include

urlpatterns = [
    # 1. Inkludera alla URL:er från accounts (login, logout, register, etc.)
    path('', include('accounts.urls')), 
    
    # 2. Inkludera alla URL:er från home-appen (hemsidan, om oss, etc.)
    path('', include('home.urls')), 
    
    # Obs: Om du har en admin-länk här, ta bort den från Mediap/urls.py
]