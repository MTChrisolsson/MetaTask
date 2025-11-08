# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),

    # Inloggning
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    
    # Utloggning
    path('logout/', views.logout_view, name='logout'),

    # Registrering
    path('register/', views.register_view, name='register'),
    
    path('organizations/<slug:slug>/add-member/', views.organization_add_member, name='org_add_member'),

    
    # Här kan du senare lägga till password reset, etc.
]