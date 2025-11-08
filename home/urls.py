# home/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_index, name='home_index'),
    # lägg till fler URL-er för mediap.org här
]