from django.urls import path
from . import views

urlpatterns = [
    path('<date>/Redirect/', views.Redirect, name='QuickRedirect'),
    path('<date>/', views.Report, name='Report'),
    path('', views.ReportRedirect, name='Reportenter'),
]