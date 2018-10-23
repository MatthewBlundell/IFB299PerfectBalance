from Search.models import User
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


def Search(input):

    #Splitting the search term into each individual term to begin processing
    inputsplit = input.split()
    CustomerList = []

    #Using regular expression to easily search through multiple potential things to look for in a vehicle search
    #duplicates are okay because they get filtered out later in the process
    #Each word in the search string is first searched against these potential look ups
    try:
        for z in inputsplit:
            for i in User.objects.filter(userid__iregex=r'' + z):
                CustomerList.append(i)
            for i in User.objects.filter(name__iregex=r'' + z):
                CustomerList.append(i)
            for i in User.objects.filter(username__iregex=r'' + z):
                CustomerList.append(i)
            for i in User.objects.filter(authenticationlevel__iregex=r'' + z):
                CustomerList.append(i)
            for i in User.objects.filter(birthday__iregex=r'' + z):
                CustomerList.append(i)
            for i in User.objects.filter(phone__iregex=r'' + z):
                CustomerList.append(i)
            for i in User.objects.filter(address__iregex=r'' + z):
                CustomerList.append(i)
    except:
        return CustomerList

    return CustomerList


def ProfilePortal(request):
    name = -1
    userid = -1
    auth = -1

    #redirect if user isn't authenicated or an admin
    if request.session.has_key('email'):
        uservar = User.objects.get(username=request.session['email'])
        name = uservar.name
        userid = uservar.userid
        auth = uservar.authenticationlevel
        if uservar.authenticationlevel != 1:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


    #grab current search on page and run through the user database
    searchfield = request.GET.get('SearchField')

    if searchfield == None:
        Customers = User.objects.all()
    else:
        Customers = Search(searchfield)

    #Remove any duplicates from the search
    Customers = DupeRemover(Customers)

    template = loader.get_template('ProfilePortal.html')
    context = {
        'name': name,
        'userid': userid,
        'authlevel': auth,
        'Customers': Customers,
    }
    return HttpResponse(template.render(context, request))