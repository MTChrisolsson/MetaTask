# Mediap/root_urls.py
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    # Add admin only on the main site
    path('admin/', admin.site.urls, name='admin'),
    # 1. Include URLs from accounts (login, logout, register, etc.)
    path('', include('accounts.urls')), 
    
    # 2. Inkludera alla URL:er från home-appen (hemsidan, om oss, etc.)
    path('', include('home.urls')), 
    
    # 3. Inkludera alla URL:er från cflows-appen (bilhantering, etc.)
    path('cflows/', include('cflows.urls')),
    # Obs: Om du har en admin-länk här, ta bort den från Mediap/urls.py
]