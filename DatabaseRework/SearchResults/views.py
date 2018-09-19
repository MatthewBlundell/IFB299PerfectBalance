from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from Search.models import Vehicle
from django.shortcuts import get_object_or_404

def search(request):
    SearchQuery = request.GET.get('SearchField')
    if SearchQuery == None:
        SearchQuery = ""
    VehicleList = []

    for i in Vehicle.objects.filter(carmake=SearchQuery):
        VehicleList.append(i)


    template = loader.get_template('SearchPage.html')
    context = {
        'Search': SearchQuery,
        'VehicleList': VehicleList
    }

    return HttpResponse(template.render(context, request))


def returner(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'));