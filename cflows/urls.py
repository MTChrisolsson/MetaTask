# cflows/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='cflows_index'),
    path('cars/', views.CarListView.as_view(), name='car_list'),
    path('cars/create/', views.create_car, name='car_create'),
    path('cars/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('cars/filter/', views.car_filter, name='car_filter'),
    
]