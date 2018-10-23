from django.urls import path
from . import views

# url paths that utilise functions in views.py
# visit views.py for more information on the function specifics.
urlpatterns = [
    path('<date>/<weekNum>/Redirect/', views.Redirect, name='QuickRedirect'),
    path('<date>/<weekNum>/', views.Report, name='Report'),
    path('', views.ReportRedirect, name='Reportenter'),
]
