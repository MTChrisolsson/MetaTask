# cflows/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='cflows_index'),
    #path('cars/', views.car_list, name='car_list'),
    # lägg till fler URL-er för cflows.mediap.org här
]