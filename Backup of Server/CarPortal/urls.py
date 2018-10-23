from django.urls import path
from . import views

urlpatterns = [
    path('', views.CarPortal, name='CarPortal'),
]