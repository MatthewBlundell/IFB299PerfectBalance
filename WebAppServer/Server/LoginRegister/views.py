from django.template import loader
from Search.models import User
from django.http import HttpResponse, HttpResponseRedirect
import re

#Verification for email input
def CheckEmail(input):
    m = re.search(r'.+@.+\.com', input)
    if m:
        return True
    else:
        return False

#Verification for name input
def CheckName(input):
    m = re.search(r'[A-Za-z]+ [A-za-z]+', input)
    if m:
        return True
    else:
        return False

#Confirms that input is a number
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

#Confirms password is above 8 characters
def CheckPass(input):
    if len(input) >= 8:
        return True
    else:
        return False

#Confirms both password inputs are equal
def CheckRePass(input, input2):
    if input == input2:
        return True
    else:
        return False

def Loginenter(request):
    #input default values
    Check = False
    NameVerify = True
    NumberVerify = True
    EmailVerify = True
    PasswordVerify = True
    PasswordReVerify = True

    #redirect if user already logged in
    if request.session.has_key('email'):
        return HttpResponseRedirect('http://127.0.0.1:8000/');

    #If a failed login attemp is found this will warn user
    if request.session.has_key('Login'):
        Check = True
        request.session.flush()

    #default values for registering
    registerverify = True
    registerexists = False

    #Grab and process the request
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
        EmailVerify = CheckEmail(Email)
        PasswordVerify = CheckPass(Password)
        PasswordReVerify = CheckRePass(PasswordRe, Password)

        #convert to enum type
        if Gender == 'male':
            TrueGender = 'M'
        else:
            TrueGender = 'F'

        #complete verification and submit to database to be created
        if NameVerify and NumberVerify and EmailVerify and PasswordReVerify and PasswordReVerify:
            if len(User.objects.filter(username=Email)) > 0:
                registerexists = True
            if registerexists != True:
                try:
                    User.objects.create(name=Name, phone=Number, address=Address, birthday=DOB, occupation=Occupation, gender=TrueGender, username=Email, password=Password, authenticationlevel=0)
                    request.session['email'] = Email
                    return HttpResponseRedirect('http://127.0.0.1:8000/');
                except:
                    registerverify = False



    template = loader.get_template('RegisterForm.html')
    context = {
        'register': registerverify,
        'exists': registerexists,
        'Check': Check,
        'session': request.session.has_key('email'),
        'NameVerify': NameVerify,
        'NumberVerify': NumberVerify,
        'EmailVerify': EmailVerify,
        'PasswordVerify': PasswordVerify,
        'PasswordReVerify': PasswordReVerify,
    }
    return HttpResponse(template.render(context, request))





def RegisterAttempt():
    pass