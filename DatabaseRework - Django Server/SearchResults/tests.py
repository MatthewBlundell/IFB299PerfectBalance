from django.test import TestCase
from Search.models import test_Vehicle, test_Order
# Create your tests here.
class SearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_Vehicle.objects.create(carmake="BMW", model="Super Model", series="Super Series", year=2018)
        test_Vehicle.objects.create(carmake="SAAB", model="Linear", series="Fusion", year=2020)
        test_Vehicle.objects.create(carmake="SAAB", model="BAAS", series="Unknown", year=2017)
        test_Order.objects.create(carid=test_Vehicle.objects.get(carmake="BMW"), createdate=20181023, pickupdate=20181023, returndate=20181025)

    def test_Empty_Search(self):
        self.assertIs(len(StringSearch("")), 0)

    def test_BMW_Search(self):
        self.assertEqual(StringSearch("BMW")[0], test_Vehicle.objects.get(carmake="BMW"))

    def test_Not_BMW(self):
        self.assertNotIn(test_Vehicle.objects.get(carmake="BMW"), StringSearch("SAAB"))

    def test_Filter_Empty(self):
        Filters = [0,0,0,0,0,0]
        List = []
        self.assertEqual(FilterSearch(List, Filters), [])

    def test_Filter_Single_Filter_Empty_List(self):
        Filters = [1,0,0,0,0,0]
        List = []
        self.assertIn(test_Vehicle.objects.get(carmake="BMW"), FilterSearch(List, Filters))

    def test_Filter_Remove_Items_that_dont_match_Filter(self):
        Filters = [1,0,0,0,0,0]
        List = []
        for i in test_Vehicle.objects.filter(carmake="SAAB"):
            List.append(i)
        self.assertNotIn(test_Vehicle.objects.filter(carmake="SAAB"), FilterSearch(List, Filters))

    def test_Availability_search_on_list_no_orders_between_dates(self):
        List = test_Vehicle.objects.all()
        self.assertEqual(list(test_Vehicle.objects.all()), list(AvailabilitySearch(List, 20070201, 20070205)))

    def test_Search_Between_Dates_Order_Exists(self):
        List = list(test_Vehicle.objects.all())
        self.assertNotIn(test_Vehicle.objects.get(carmake="BMW"), AvailabilitySearch(List, 20181023, 20181029))




def StringSearch(input):

    # Splitting the search term into each individual term to begin processing
    inputsplit = input.split()
    vehiclelist = []

    # Using regular expression to easily search through multiple potential things to look for in a vehicle search
    # duplicates are okay because they get filtered out later in the process
    # Each word in the search string is first searched against these potential look ups

    for z in inputsplit:
        for i in test_Vehicle.objects.filter(carmake__iregex=r'' + z):
            vehiclelist.append(i)
        for i in test_Vehicle.objects.filter(model__iregex=r'' + z):
            vehiclelist.append(i)
        for i in test_Vehicle.objects.filter(series__iregex=r'' + z):
            vehiclelist.append(i)
        for i in test_Vehicle.objects.filter(standardtransmission__iregex=r'' + z):
            vehiclelist.append(i)
        for i in test_Vehicle.objects.filter(carbodytype__iregex=r'' + z):
            vehiclelist.append(i)
        for i in test_Vehicle.objects.filter(year__iregex=r'' + z):
            vehiclelist.append(i)

    return vehiclelist




#defining all the filter options for the filter search
Brand = ['BMW', 'VOLKSWAGEN', 'MERCEDES-BENZ', 'MAZDA', 'DATSUN', 'ALFA ROMEO', 'VOLVO', 'RENAULT', 'LAND ROVER',
         'SAAB', 'NISSAN', 'PEUGOT', 'CHRYSLER']

Body = ['4D WAGON', '3D HARDBACK', '2D HARDBACK', '2D HARDTOP', '3D HATCHBACK', '4D SEDAN', '2D COUPE']

Fuel = ['DIESEL TURBO F/INJ', 'DIESEL TURBO', 'MULTI POINT F/INJ', 'TURBO CDI', 'ELECTRONIC F/INJ', 'CARB',
        'SINGLE POINT F/INJ', 'TURBO MPFI', 'SUPER CHARGED MPFI']

Seats = [2, 3, 4, 5, 6, 7]

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
        for i in test_Vehicle.objects.filter(carmake=Brand[filters[0]-1]):
            temp2.append(i)
    #add vehicles with filter type for body
    if filters[1] > 0:
        for i in test_Vehicle.objects.filter(carbodytype=Body[filters[1]-1]):
            temp2.append(i)
    #add vehicles with filter type for seating capacity
    if filters[2] > 0:
        if filters[2] == 6:
            for i in test_Vehicle.objects.filter(seatingcapacity__in=[7, 8, 9, 10, 11, 12, 13, 14, 15, 16]):
                temp2.append(i)
        else:
            for i in test_Vehicle.objects.filter(seatingcapacity=Seats[filters[2]-1]):
                temp2.append(i)
    #add vehicles with filter for fuel processing type
    if filters[3] > 0:
        for i in test_Vehicle.objects.filter(fuelsystem=Fuel[filters[3]-1]):
            temp2.append(i)
    #add vehicles with price above minimum set
    if filters[4] > 0:
        for i in test_Vehicle.objects.filter(price__lte=filters[4]):
            temp2.append(i)
    #add vehicles with price below minimum set
    if filters[5] > 0:
        for i in test_Vehicle.objects.filter(price__gte=filters[5]):
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
    orderlist = test_Order.objects.filter(pickupdate__range=(startdate, enddate), returndate__range=(startdate, enddate))\
        .extra({'carid_int': "CAST(carid as UNSIGNED)"})

    #if any of the current vehicles in the list are in a current order between these dates, the vehicle will be removed
    for z in range(len(orderlist)):
        for i in range(len(VehicleList)-1,-1,-1):
            if int(VehicleList[i].carid) == orderlist[z].carid_int:
                del VehicleList[i]

    return VehicleList