from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<id>/', views.InfoCar, name='InfoCar'),
    path('<id>/Rent/', include('RentedPage.urls')),
]