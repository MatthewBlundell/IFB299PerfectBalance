from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from Search.models import User, Vehicle

Brand = ['BMW', 'VOLKSWAGEN', 'MERCEDES-BENZ', 'MAZDA', 'DATSUN', 'ALFA ROMEO', 'VOLVO', 'RENAULT', 'LAND ROVER',
         'SAAB', 'NISSAN', 'PEUGOT', 'CHRYSLER']

Body = ['4D WAGON', '3D HARDBACK', '2D HARDBACK', '2D HARDTOP', '3D HATCHBACK', '4D SEDAN', '2D COUPE']

Fuel = ['DIESEL TURBO F/INJ', 'DIESEL TURBO', 'MULTI POINT F/INJ', 'TURBO CDI', 'ELECTRONIC F/INJ', 'CARB',
        'SINGLE POINT F/INJ', 'TURBO MPFI', 'SUPER CHARGED MPFI']

Seats = [2, 3, 4, 5, 6, 7]


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

    Filters = [0, 0, 0, 0, 0, 0]


    Brand = request.GET.get('Brand')
    Body = request.GET.get('Body')
    Seats = request.GET.get('Seats')
    Fuel = request.GET.get('Fuel')
    Min = request.GET.get('Min')
    Max = request.GET.get('Max')


    if Brand != "None" and Body != "None" and Seats != "None" and Fuel != "None" and Min != "None" and Max != None:
        Filters = [int(Brand), int(Body), int(Seats), int(Fuel), int(Min), int(Max)]
        VehicleList = FilterSearch(VehicleList, Filters)

    DupeRemover(VehicleList)

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
        'Brand': Filters[0],
        'Body': Filters[1],
        'Seats': Filters[2],
        'Fuel': Filters[3],
        'Min': Filters[4],
        'Max': Filters[5],
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

    for i in Vehicle.objects.filter(carmake=r'' + input):
        vehiclelist.append(i)
    for i in Vehicle.objects.filter(model=r'' + input):
        vehiclelist.append(i)
    for i in Vehicle.objects.filter(series=r'' + input):
        vehiclelist.append(i)
    for i in Vehicle.objects.filter(standardtransmission=r'' + input):
        vehiclelist.append(i)
    for i in Vehicle.objects.filter(carbodytype=r'' + input):
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

    return vehiclelist

def CheckFilters(filters, temp2):
    temp = temp2
    if filters[0] > 0:
        for i in range(len(temp)-1, -1, -1):
            if temp[i].carmake != Brand[filters[0]-1]:
                del temp[i]

    if filters[1] > 0:
        for i in range(len(temp)-1, -1, -1):
            if temp[i].carbodytype != Body[filters[1]-1]:
                del temp[i]

    if filters[2] > 0:
        if filters[2] == 6:
            for i in range(len(temp)-1, -1, -1):
                allchecks = True
                for z in range(7,20):
                    if temp[i].seatingcapacity == z:
                        allchecks = False
                    if allchecks == True:
                        del temp[i]

        else:
            for i in range(len(temp)-1, -1, -1):
                if temp[i].seatingcapacity != Seats[filters[2]-1]:
                    del temp[i]

    if filters[3] > 0:
        for i in range(len(temp)-1, -1, -1):
            if temp[i].fuelsystem != Fuel[filters[3]-1]:
                del temp[i]

    if filters[4] > 0 or filters[5] > 0:
        for i in range(len(temp)-1, -1, -1):
            if temp[i].price < filters[4] or temp[i].price > filters[5]:
                del temp[i]

    return temp


def FilterSearch(input, filters):
    temp = CheckFilters(filters, input)

    temp2 = []
    if filters[0] > 0:
        for i in Vehicle.objects.filter(carmake=Brand[filters[0]-1]):
            temp2.append(i)

    if filters[1] > 0:
        for i in Vehicle.objects.filter(carbodytype=Body[filters[1]-1]):
            temp2.append(i)

    if filters[2] > 0:
        if filters[2] == 6:
            for i in Vehicle.objects.filter(seatingcapacity=[7, 8, 9, 10, 11, 12, 13, 14, 15, 16]):
                temp2.append(i)
        else:
            for i in Vehicle.objects.filter(seatingcapacity=Seats[filters[2]-1]):
                temp2.append(i)

    if filters[3] > 0:
        for i in Vehicle.objects.filter(fuelsystem=Fuel[filters[3]-1]):
            temp2.append(i)

    if filters[4] > 0:
        for i in Vehicle.objects.filter(price__lte=filters[4]):
            temp2.append(i)

    if filters[5] > 0:
        for i in Vehicle.objects.filter(price__gte=filters[5]):
            temp2.append(i)

    temp2 = CheckFilters(filters, temp2)

    for i in temp2:
        temp.append(i)

    return temp

def AvaibilitySearch(input):
    pass

def returner(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'));

def DupeRemover(input):
    output = []
    seen = set()
    for value in input:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output