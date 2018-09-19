from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from Search.models import Order, Vehicle, User
# Create your views here.

def home(request):
    template = loader.get_template('home.html')
    context = {}

    return HttpResponse(template.render(context, request))





