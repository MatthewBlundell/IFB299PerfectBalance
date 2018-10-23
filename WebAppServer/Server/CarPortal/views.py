from Search.models import Vehicle, User
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader


#runs through current list of vehicles and removes any duplicates from the process
def DupeRemover(input):
    output = []
    seen = set()
    for value in input:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

#quick searcher to help minimize the list
def Search(input):

    #Splitting the search term into each individual term to begin processing
    inputsplit = input.split()
    vehiclelist = []

    #Using regular expression to easily search through multiple potential things to look for in a vehicle search
    #duplicates are okay because they get filtered out later in the process
    #Each word in the search string is first searched against these potential look ups
    try:
        for z in inputsplit:
            for i in Vehicle.objects.filter(carid__iregex=r'' + z):
                vehiclelist.append(i)
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

def CarPortal(request):
    #default values for user session
    name = -1
    userid = -1
    auth = -1

    #checks that user is in fact an admin
    #returns to referer if they aern't an admin or not logged in
    if request.session.has_key('email'):
        uservar = User.objects.get(username=request.session['email'])
        name = uservar.name
        userid = uservar.userid
        auth = uservar.authenticationlevel
        if uservar.authenticationlevel != 1:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    #If a search has been done this will grab the search string
    searchfield = request.GET.get('SearchField')

    #if no search grab all vehicles or begin searching
    if searchfield == None:
        VehicleList = Vehicle.objects.all()
    else:
        VehicleList = Search(searchfield)

    #Remove duplicates from search
    VehicleList = DupeRemover(VehicleList)

    template = loader.get_template('CarPortal.html')
    context = {
        'name': name,
        'userid': userid,
        'authlevel': auth,
        'Vehicles': VehicleList,
    }
    return HttpResponse(template.render(context, request))