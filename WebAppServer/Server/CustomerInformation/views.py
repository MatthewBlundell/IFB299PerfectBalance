from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from Search.models import User, Order, Vehicle
from django.shortcuts import get_object_or_404

# Create your views here.
def InfoUser(request, profile):
    #user session default information
    Check = False
    name = -1
    userid = -1
    auth = -1

    #if failed login the page uses the Check variable to notify the user
    if request.session.has_key('Login'):
        Check = True
        request.session.flush()

    #confirms that the user is either an admin or they are looking at there own page
    if request.session.has_key('email'):
        uservar = User.objects.get(username=request.session['email'])
        if uservar.authenticationlevel != 1:
            if uservar.userid != int(profile):
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    #saves curren session details for displaying
    if request.session.has_key('email'):
        uservar = User.objects.get(username=request.session['email'])
        name = uservar.name
        userid = uservar.userid
        auth = uservar.authenticationlevel

    person = get_object_or_404(User, userid=profile)

    #List objects holds all rentals and customer information
    vehiclelist = []
    count = 0
    orderlist = []
    cost = []
    for z in Order.objects.filter(userid=person.userid).extra(
            {'carid_uint': "CAST(carid as UNSIGNED)"}):
        orderlist.append(z)
        vehiclelist.append(Vehicle.objects.get(carid=z.carid_uint))
        count += 1

    #calculating costs per order
    for i in vehiclelist:
        cost.append(int(int(i.price)*0.001))

    together = zip(vehiclelist, orderlist, cost)


    template = loader.get_template('CustomerProfile.html')
    context = {
        'Name': person.name,
        'Number': person.phone,
        'Birthday': person.birthday,
        'Address': person.address,
        'together': together,
        'Count': count,
        'name': name,
        'userid': userid,
        'authlevel': auth,
        'Check': Check,
        'session': request.session.has_key('email'),
    }

    return HttpResponse(template.render(context, request))


def home(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))