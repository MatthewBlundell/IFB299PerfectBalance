from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from Search.models import Order, Vehicle, User
from django.shortcuts import redirect

def LoginForm(request):
    Check = False

    if request.session.has_key('Login'):
        Check = True
        request.session.flush()

    if request.session.has_key('email'):
        return HttpResponseRedirect('.././')

    template = loader.get_template('LoginForm.html')
    context = {
        'Check': Check,

    }
    return HttpResponse(template.render(context, request))