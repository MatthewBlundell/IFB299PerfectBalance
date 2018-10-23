from django.urls import path
from . import views

urlpatterns = [
    path('<carid>/', views.CarReport, name='CarReportenter'),
]