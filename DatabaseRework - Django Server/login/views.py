from django.shortcuts import render
from Search.models import User
from django.http import JsonResponse, HttpResponseRedirect


def Login(request):
    if request.method == "POST":
        if request.POST.get('action') == 'login':
            if (LoginAttempt(request.POST.get('email'), request.POST.get('password'))):
                print("Success")
                request.session['email'] = request.POST.get('email')
                response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                return response
    Response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    request.session['Login'] = "Failed"
    print("Failed")
    return Response

# Create your views here.
def LoginAttempt(Username, Pass):
    try:
        Userobject = User.objects.get(username=Username)
        if (Userobject.password == Pass):
            return True
        else:
            return False
    except:
        return False