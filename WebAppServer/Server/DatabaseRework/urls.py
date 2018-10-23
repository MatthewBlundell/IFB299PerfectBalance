"""DatabaseRework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, re_path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    re_path(r'^[Rr][Ee][Pp][oO][Rr][tT][Ii][Nn][Gg]/', include('Reporting.urls')),
    re_path(r'^[Cc][Aa][Rr][_][Ii][Nn][Ff][Oo][Rr][Mm][Aa][Tt][Ii][Oo][Nn]/', include('CarInformation.urls')),
    re_path(r'^[Ss][Ee][Aa][Rr][Cc][Hh]/', include('SearchResults.urls')),
    re_path(r'^[Pp][Rr][Oo][Ff][Ii][Ll][Ee]/', include('CustomerInformation.urls')),
    re_path(r'^[Rr][Ee][Gg][Ii][Ss][Tt][Ee][Rr]/', include('LoginRegister.urls')),
    re_path(r'^[Ll][Oo][Gg][Ii][Nn]/', include("login.urls")),
    re_path(r'[Ll][Oo][Gg][Oo][Uu][Tt]/', include('Logout.urls')),
    re_path(r'[Cc][Aa][Rr][_][Rr][Ee][Pp][Oo][Rr][Tt]/', include('CarReport.urls')),
    re_path(r'[Ll][Oo][Gg][Ii][Nn][_][Ff][Oo][Rr][Mm]/', include('LoginPage.urls')),
    re_path(r'[Cc][Aa][Rr][Pp][Oo][Rr][Tt][Aa][Ll]/', include('CarPortal.urls')),
    re_path(r'[Pp][Rr][Oo][Ff][Ii][Ll][Ee][Pp][Oo][Rr][Tt][Aa][Ll]/', include('ProfilePortal.urls')),
]
