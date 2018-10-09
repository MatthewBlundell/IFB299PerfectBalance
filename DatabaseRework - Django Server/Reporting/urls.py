from django.urls import path
from . import views

urlpatterns = [
    path('<datereport>/', views.Report, name='Report'),
    path('', views.Reportenter, name='Reportenter'),
]