from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProfilePortal, name='ProfilePortal'),
]