from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.

def index(request):
    return render(request,'index.html')

    #return HttpResponse("<p><b>Login details for <a href=\"/admin/\">/admin/</b></a></p>"
     #                   "<p><b>Username:</b> admin</p>"
      #                  "<p><b>Password:</b> password</p>")
