from django.urls import path
from . import views

urlpatterns = [
    path('', views.Rent, name='Rent'),
    path('Rent/', views.BeginRent, name='BeginRent'),
]