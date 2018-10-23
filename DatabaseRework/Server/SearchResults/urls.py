from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.search, name='search'),
    re_path(r'.*/*', views.returner, name='returner')
]