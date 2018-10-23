from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from Search.models import User, Vehicle, Order
import datetime

#defining all the filter options for the filter search
Brand = ['BMW', 'VOLKSWAGEN', 'MERCEDES-BENZ', 'MAZDA', 'DATSUN', 'ALFA ROMEO', 'VOLVO', 'RENAULT', 'LAND ROVER',
         'SAAB', 'NISSAN', 'PEUGOT', 'CHRYSLER']

Body = ['4D WAGON', '3D HARDBACK', '2D HARDBACK', '2D HARDTOP', '3D HATCHBACK', '4D SEDAN', '2D COUPE']

Fuel = ['DIESEL TURBO F/INJ', 'DIESEL TURBO', 'MULTI POINT F/INJ', 'TURBO CDI', 'ELECTRONIC F/INJ', 'CARB',
        'SINGLE POINT F/INJ', 'TURBO MPFI', 'SUPER CHARGED MPFI']

Seats = [2, 3, 4, 5, 6, 7]


def search(request):
    Check = False

    #Checks if failed login has occured and updates the page if it comes back true
    if request.session.has_key('Login'):
        Check = True
        request.session.flush()

    name = -1
    userid = -1
    auth = -1

    #sets variables for the user if they are logged in
    if request.session.has_key('email'):
        uservar = User.objects.get(username=request.session['email'])
        name = uservar.name
        userid = uservar.userid
        auth = uservar.authenticationlevel

    #begin searching. sets the searchquery to show on the webpage when requested so that it doesn't just dissapear
    VehicleList = []
    SearchQuery = request.GET.get('SearchField')
    if SearchQuery == None:
        SearchQuery = ""
    else:
        VehicleList = StringSearch(SearchQuery.lower())

    #default filter values
    Filters = [0, 0, 0, 0, 0, 0]


    #getting filters from search request
    Brand = request.GET.get('Brand')
    Body = request.GET.get('Body')
    Seats = request.GET.get('Seats')
    Fuel = request.GET.get('Fuel')
    Min = request.GET.get('Min')
    Max = request.GET.get('Max')

    StartDate = request.GET.get('StartDate')
    EndDate = request.GET.get('EndDate')

    #safety if statement if the filters are missing from the url
    if Brand != None and Body != None and Seats != None and Fuel != None and Min != None and Max != None:
        Filters = [int(Brand), int(Body), int(Seats), int(Fuel), int(Min), int(Max)]
        #run current list of vehicles through the filter sort function
        VehicleList = FilterSearch(VehicleList, Filters)


    curDateMax = None
    curDateMin = None

    if StartDate != None and EndDate != None:
        today = datetime.datetime.today().strftime('%Y%m%d')
        startdate = StartDate[0:4] + StartDate[5:7] + StartDate[8:11]
        enddate = EndDate[0:4] + EndDate[5:7] + EndDate[8:11]
        # safety for the url being edited in the get request
        if startdate >= today and enddate >= today:
            VehicleList = AvailabilitySearch(VehicleList, startdate, enddate)
            curDateMin = StartDate
            curDateMax = EndDate


    #remove all duplicates in the vehicle list
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
        'curDateMax': curDateMax,
        'curDateMin': curDateMin,
        'MinDate': datetime.datetime.today().strftime('%Y-%m-%d'),
    }
    return HttpResponse(template.render(context, request))

#confirms that the input is a number
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



#process for the specific search functionality

def StringSearch(input):

    #Splitting the search term into each individual term to begin processing
    inputsplit = input.split()
    vehiclelist = []

    #Using regular expression to easily search through multiple potential things to look for in a vehicle search
    #duplicates are okay because they get filtered out later in the process
    #Each word in the search string is first searched against these potential look ups

    try:
        for z in inputsplit:
            for i in Vehicle.objects.filter(carmake__iregex=r'' + z):
                vehiclelist.append(i)
            for i in Vehicle.objects.filter(model__iregex=r'' + z):
                vehiclelist.append(i)
            for i in Vehicle.objects.filter(series__iregex=r'' + z):
                vehiclelist.append(i)
            for i in Vehicle.objects.filter(standardtransmission__iregex=r'' + z):
                vehiclelist.append(i)
            for i in Vehicle.objects.filter(carbodytype__iregex=r'' + z):
                vehiclelist.append(i)
            for i in Vehicle.objects.filter(year__iregex=r'' + z):
                vehiclelist.append(i)
    except:
        return vehiclelist

    return vehiclelist

def CheckFilters(filters, currentlist):
    #Takes the current list of vehicles and begins filtering it down through all the set filters
    temp = currentlist
    #check for brand filter
    if filters[0] > 0:
        for i in range(len(temp)-1, -1, -1):
            if temp[i].carmake != Brand[filters[0]-1]:
                del temp[i]
    #check for body filter
    if filters[1] > 0:
        for i in range(len(temp)-1, -1, -1):
            if temp[i].carbodytype != Body[filters[1]-1]:
                del temp[i]
    #check for seating capacity filter
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
    #check for fuelsystem type filter
    if filters[3] > 0:
        for i in range(len(temp)-1, -1, -1):
            if temp[i].fuelsystem != Fuel[filters[3]-1]:
                del temp[i]

    #check for price range filter
    if filters[4] > 0 or filters[5] > 0:
        for i in range(len(temp)-1, -1, -1):
            if temp[i].price < filters[4] or temp[i].price > filters[5]:
                del temp[i]

    return temp


def FilterSearch(input, filters):
    #takes current list of filters and runs it through the filter checker function
    temp = CheckFilters(filters, input)

    #creates a list from the current filters being made just incase the search field was empty
    temp2 = []
    #add vehicles with filter type for brand
    if filters[0] > 0:
        for i in Vehicle.objects.filter(carmake=Brand[filters[0]-1]):
            temp2.append(i)
    #add vehicles with filter type for body
    if filters[1] > 0:
        for i in Vehicle.objects.filter(carbodytype=Body[filters[1]-1]):
            temp2.append(i)
    #add vehicles with filter type for seating capacity
    if filters[2] > 0:
        if filters[2] == 6:
            for i in Vehicle.objects.filter(seatingcapacity__in=[7, 8, 9, 10, 11, 12, 13, 14, 15, 16]):
                temp2.append(i)
        else:
            for i in Vehicle.objects.filter(seatingcapacity=Seats[filters[2]-1]):
                temp2.append(i)
    #add vehicles with filter for fuel processing type
    if filters[3] > 0:
        for i in Vehicle.objects.filter(fuelsystem=Fuel[filters[3]-1]):
            temp2.append(i)
    #add vehicles with price above minimum set
    if filters[4] > 0:
        for i in Vehicle.objects.filter(price__lte=filters[4]):
            temp2.append(i)
    #add vehicles with price below minimum set
    if filters[5] > 0:
        for i in Vehicle.objects.filter(price__gte=filters[5]):
            temp2.append(i)

    #run list made from filters through filters to ensure that they matcha all filters and not just their own
    temp2 = CheckFilters(filters, temp2)

    for i in temp2:
        temp.append(i)

    #returns list that all matched the filters
    return temp

def AvailabilitySearch(vehiclelist, startdate, enddate):
    VehicleList = vehiclelist

    #Complete list of orders between the two dates
    orderlist = Order.objects.filter(pickupdate__range=(startdate, enddate), returndate__range=(startdate, enddate))\
        .extra({'carid_int': "CAST(carid as UNSIGNED)"})

    #if any of the current vehicles in the list are in a current order between these dates, the vehicle will be removed
    for z in range(len(orderlist)):
        for i in range(len(VehicleList)-1,-1,-1):
            if int(VehicleList[i].carid) == orderlist[z].carid_int:
                del VehicleList[i]

    return VehicleList




def returner(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'));

#runs through current list of vehicles and removes any duplicates from the process
def DupeRemover(input):
    output = []
    seen = set()
    for value in input:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output
