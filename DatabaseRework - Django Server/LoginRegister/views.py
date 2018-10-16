from django.template import loader
from Search.models import User
from django.http import HttpResponse, HttpResponseRedirect
import re

def CheckString(input):
    pass

def CheckName(input):
    m = re.search(r'[A-Za-z]+ [A-za-z]+', input)
    if m:
        return True
    else:
        return False

def CheckInt(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def CheckDate(input):
    pass

def CheckUser(input):
    pass

def CheckPass(input):
    pass

def Loginenter(request):
    Check = False
    NameVerify = True
    if request.session.has_key('email'):
        return HttpResponseRedirect('http://127.0.0.1:8000/');

    if request.session.has_key('Login'):
        Check = True
        request.session.flush()

    registerverify = True
    registerexists = False
    if request.method == "POST":
        Name = request.POST.get('Name')
        Number = request.POST.get('Number')
        Address = request.POST.get('Address')
        DOB = request.POST.get('DOB')
        Occupation = request.POST.get('Occupation')
        Gender = request.POST.get('Gender')
        Email = request.POST.get('Email')
        Password = request.POST.get('Password')
        PasswordRe = request.POST.get('PasswordRe')
        NameVerify = CheckName(Name)
        NumberVerify = CheckInt(Number)
    template = loader.get_template('RegisterForm.html')
    context = {
        'register': registerverify,
        'exists': registerexists,
        'Check': Check,
        'session': request.session.has_key('email'),
        'NameVerify': NameVerify,
        'NumberVerify': NumberVerify,
    }
    return HttpResponse(template.render(context, request))





def RegisterAttempt():
    pass