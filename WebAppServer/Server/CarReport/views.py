from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from Search.models import Order, Vehicle, User


def CarReport(request, carid):
    #Session variables for user
    name = -1
    userid = -1
    auth = -1

    #checks user is logged in and is an administrator. Will redirect if not.
    if request.session.has_key('email'):
        uservar = User.objects.get(username=request.session['email'])
        name = uservar.name
        userid = uservar.userid
        auth = uservar.authenticationlevel
        if uservar.authenticationlevel != 1:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    #grabs vehicle object and all orders associated with the vehicle
    vehicle = Vehicle.objects.get(carid=carid)
    orders = Order.objects.filter(carid=carid)

    #finds people that ordered vehicle
    people = []
    for i in orders:
        people.append(User.objects.get(userid=str(i.userid)))

    #combine into one list
    mix = zip(orders, people)

    template = loader.get_template('CarReport.html')
    context = {
        'carid': carid,
        'Make': vehicle.carmake,
        'Model': vehicle.model,
        'Year': vehicle.year,
        'Series': vehicle.series,
        'Price': vehicle.price,
        'Fuel': vehicle.fuelsystem,
        'Seating': vehicle.seatingcapacity,
        'Mix': mix,
        'name': name,
    }
    return HttpResponse(template.render(context, request))
