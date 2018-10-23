from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from Search.models import User, Vehicle, Store, Order
from django.shortcuts import get_object_or_404
import datetime


def Rent(request, id):
    if request.method == 'GET':
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    DateStart = request.POST.get('pickupdate')
    DateEnd = request.POST.get('returndate')
    EndLocation = request.POST.get('endlocation')


    Locations = ['Coffs Harbour', 'Darlinghurst', 'Goulburn', 'Melbourne', 'Gold Coast', 'Springwood']


    if DateStart == "" or DateEnd == "" or EndLocation == "0":
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    Reservable = True
    name = -1
    userid = -1
    auth = -1

    if request.session.has_key('email'):
        uservar = User.objects.get(username=request.session['email'])
        name = uservar.name
        userid = uservar.userid
        auth = uservar.authenticationlevel

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    today = datetime.datetime.today().strftime('%Y%m%d')
    if int(DateStart[0:4]+DateStart[5:7]+DateStart[8:11]) < int(today) or int(DateEnd[0:4]+DateEnd[5:7]+DateEnd[8:11]) < int(today):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    EndLocation = Locations[int(EndLocation) - 1]
    car = get_object_or_404(Vehicle, carid=id)



    #Complete list of orders between the two dates
    orderlist = Order.objects.filter(pickupdate__range=(int(DateStart[0:4]+DateStart[5:7]+DateStart[8:11]), int(DateEnd[0:4]+DateEnd[5:7]+DateEnd[8:11]))
                                     , returndate__range=(int(DateStart[0:4]+DateStart[5:7]+DateStart[8:11]), int(DateEnd[0:4]+DateEnd[5:7]+DateEnd[8:11])))


    for i in orderlist:
        if str(car.carid) == str(i.carid):
            Reservable = False

    orderlocation = Store.objects.get(storeid=str(car.storeid)).city

    template = loader.get_template('RentedPage.html')
    context = {
        'name': name,
        'userid': userid,
        'authlevel': auth,
        'session': request.session.has_key('email'),
        'carmake': car.carmake,
        'Model': car.model,
        'Year': car.year,
        'Fuelsystem': car.fuelsystem,
        'Transmission': car.standardtransmission,
        'Seating': car.seatingcapacity,
        'Carpower': car.carpower,
        'Location': orderlocation,
        'DatePickUp': datetime.datetime.strptime(DateStart, "%Y-%m-%d").strftime("%B %d, %Y"),
        'DateDropOff': datetime.datetime.strptime(DateEnd, "%Y-%m-%d").strftime("%B %d, %Y"),
        'LocationDrop': EndLocation,
        'Price': int(car.price)*0.001,
        'datestart':DateStart,
        'dateend':DateEnd,
        'endlocation':EndLocation,
        'Reservable':Reservable,
    }
    return HttpResponse(template.render(context, request))



def BeginRent(request, id):
    name = -1
    userid = -1
    auth = -1

    if request.session.has_key('email'):
        uservar = User.objects.get(username=request.session['email'])
        name = uservar.name
        userid = uservar.userid
        auth = uservar.authenticationlevel

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    DesiredLocation = request.POST.get('endlocation')
    DateStart = datetime.datetime.strptime(request.POST.get('pickupdate'), "%Y-%m-%d").strftime("%Y%m%d")
    DateEnd = datetime.datetime.strptime(request.POST.get('returndate'), "%Y-%m-%d").strftime("%Y%m%d")

    car = Vehicle.objects.get(carid=id)


    orderlocation = Store.objects.get(storeid=str(car.storeid))
    dropofflocation = Store.objects.get(city__contains=DesiredLocation)
    Today = datetime.datetime.today().strftime('%Y%m%d')

    Order.objects.create(userid=uservar, carid=car, createdate=Today, pickupdate=DateStart, pickupstore=orderlocation, returndate=DateEnd, returnstore=dropofflocation)
    return HttpResponseRedirect('/../.')


