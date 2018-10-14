from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from Search.models import User, Vehicle


def search(request):
    Check = False

    if request.session.has_key('Login'):
        Check = True
        request.session.flush()

    name = -1
    userid = -1
    auth = -1
    if request.session.has_key('Login'):
        Check = True
        request.session.flush()

    if request.session.has_key('email'):
        uservar = User.objects.get(username=request.session['email'])
        name = uservar.name
        userid = uservar.userid
        auth = uservar.authenticationlevel

    VehicleList = []
    SearchQuery = request.GET.get('SearchField')
    if SearchQuery == None:
        SearchQuery = ""
    else:
        VehicleList = StringSearch(SearchQuery.lower())

    template = loader.get_template('SearchPage.html')
    context = {
        'Search': SearchQuery,
        'VehicleList': VehicleList,
        'count': len(VehicleList),
        'name': name,
        'userid': userid,
        'authlevel': auth,
        'Check': Check,
        'session': request.session.has_key('email'),
    }
    return HttpResponse(template.render(context, request))


def is_number(s):
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

def StringSearch(input):
    inputsplit = input.split()
    vehiclelist = []

    if 'land' in inputsplit:
        if 'rover' in inputsplit:
            for i in Vehicle.objects.filter(carmake="LAND ROVER"):
                vehiclelist.append(i)

    if 'alfa' in inputsplit:
        if 'romeo' in inputsplit:
            for i in Vehicle.objects.filter(carmake="ALFA ROMEO"):
                vehiclelist.append(i)

    for z in inputsplit:
        for i in Vehicle.objects.filter(carmake=z):
            vehiclelist.append(i)
        for i in Vehicle.objects.filter(model=z):
            vehiclelist.append(i)
        for i in Vehicle.objects.filter(series=z):
            vehiclelist.append(i)
        if is_number(z):
            for i in Vehicle.objects.filter(year=z):
                vehiclelist.append(i)
        for i in Vehicle.objects.filter(standardtransmission=z):
            vehiclelist.append(i)
        for i in Vehicle.objects.filter(carbodytype=z):
            vehiclelist.append(i)

    output = []
    seen = set()
    for value in vehiclelist:
        if value not in seen:
            output.append(value)
            seen.add(value)

    return output

def FilterSearch(input):
    pass

def AvaibilitySearch(input):
    pass

def returner(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'));
