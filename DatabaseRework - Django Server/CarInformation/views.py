from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from Search.models import User, Vehicle
from django.shortcuts import get_object_or_404

# Create your views here.
def InfoCar(request, id):

    Check = False

    if request.session.has_key('Login'):
        Check = True
        request.session.flush()

    name = -1
    userid = -1
    auth = -1

    if request.session.has_key('email'):
        uservar = User.objects.get(username=request.session['email'])
        name = uservar.name
        userid = uservar.userid
        auth = uservar.authenticationlevel



    car = get_object_or_404(Vehicle ,carid=id)



    template = loader.get_template('informationCar.html')
    context = {
        'carmake': car.carmake,
        'Model' : car.model,
        'Year' : car.year,
        'Fuelsystem': car.fuelsystem,
        'Transmission': car.standardtransmission,
        'Seating': car.seatingcapacity,
        'Carpower': car.carpower,
        'session': request.session.has_key('email'),
        'name': name,
        'userid': userid,
        'authlevel': auth,
        'Check': Check

    }
    return HttpResponse(template.render(context, request))


def home(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))