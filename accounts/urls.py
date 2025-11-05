# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # Inloggning
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    
    # Utloggning
    path('logout/', views.logout_view(), name='logout'),

    # Registrering
    path('register/', views.register_view, name='register'),
    
    
    # Här kan du senare lägga till password reset, etc.
]