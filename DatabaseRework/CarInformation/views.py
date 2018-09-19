from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from Search.models import Vehicle
from django.shortcuts import get_object_or_404

# Create your views here.
def InfoCar(request, id):

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

    }

    return HttpResponse(template.render(context, request))


def home(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'));