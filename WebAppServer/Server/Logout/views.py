from django.http import HttpResponseRedirect



def Logout(request):

    #clears session to log out and redirects to the home page

    if request.session.has_key('email'):
        request.session.flush()
    return HttpResponseRedirect('http://127.0.0.1:8000/');