from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import User

def index(request):
    allusers = User.objects.all()
    html = ''
    for user in allusers:
        url = "/search/" + str(user.userid) + "/"
        html += '<a href=\"' + url + '\">' + user.name + '</a><br>'
    return HttpResponse(html)


def testing(request, test):
    userlol = User.objects.get(userid=test)
    return HttpResponse('<b>Name:</b> ' + userlol.name + "<b> Occupation: </b>" + userlol.occupation)