from Search.models import User
from django.http import HttpResponseRedirect


def Login(request):
    #confirm request is a post request and starts process the post request
    #Sets a session depending on if authentication worked or failed
    if request.method == "POST":
        if request.POST.get('action') == 'login':
            if (LoginAttempt(request.POST.get('email'), request.POST.get('password'))):
                request.session['email'] = request.POST.get('email')
                response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                return response
    Response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    request.session['Login'] = "Failed"
    return Response

#attempt to find user and then authenicate that users password for logging in
def LoginAttempt(Username, Pass):
    try:
        Userobject = User.objects.get(username=Username)
        if (Userobject.password == Pass):
            return True
        else:
            return False
    except:
        return False