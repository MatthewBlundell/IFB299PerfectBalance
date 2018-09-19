from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from Search.models import User, Order, Vehicle
from django.shortcuts import get_object_or_404

# Create your views here.
def InfoUser(request, profile):
    person = get_object_or_404(User, userid=profile)
    vehiclelist = []
    count = 0

    for z in Order.objects.filter(userid=person.userid).extra(
            {'carid_uint': "CAST(carid as UNSIGNED)"}):
        vehiclelist.append(Vehicle.objects.get(carid=z.carid_uint))
        count += 1

    template = loader.get_template('CustomerProfile.html')
    context = {
        'Name': person.name,
        'Number': person.phone,
        'Birthday': person.birthday,
        'Address': person.address,
        'Vehicles': vehiclelist,
        'Count': count,
    }

    return HttpResponse(template.render(context, request))


def home(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'));