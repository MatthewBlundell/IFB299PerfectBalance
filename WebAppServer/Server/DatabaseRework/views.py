from django.http import HttpResponse
from django.template import loader
from Search.models import User
# Create your views here.

def home(request):
    #default user session values
    Check = False
    name = -1
    userid = -1
    auth = -1

    #check if user authentication failed
    if request.session.has_key('Login'):
        Check = True
        request.session.flush()

    #Check if user is already logged in a set user session variables
    if request.session.has_key('email'):
        uservar = User.objects.get(username=request.session['email'])
        name = uservar.name
        userid = uservar.userid
        auth = uservar.authenticationlevel

    template = loader.get_template('home.html')

    context = {
        'session': request.session.has_key('email'),
        'name': name,
        'userid': userid,
        'authlevel': auth,
        'Check': Check
    }

    return HttpResponse(template.render(context, request))




