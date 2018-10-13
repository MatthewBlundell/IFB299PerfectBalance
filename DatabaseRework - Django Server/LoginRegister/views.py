from django.template import loader
from Search.models import User
from django.http import HttpResponse, HttpResponseRedirect



def Loginenter(request):
    Check = False

    if request.session.has_key('email'):
        return HttpResponseRedirect('http://127.0.0.1:8000/');

    if request.session.has_key('Login'):
        Check = True
        request.session.flush()

    registerverify = True
    registerexists = False
    if request.method == "POST":
        pass

    template = loader.get_template('RegisterForm.html')
    context = {
        'register': registerverify,
        'exists': registerexists,
        'Check': Check,
        'session': request.session.has_key('email'),
    }
    return HttpResponse(template.render(context, request))





def RegisterAttempt():
    pass