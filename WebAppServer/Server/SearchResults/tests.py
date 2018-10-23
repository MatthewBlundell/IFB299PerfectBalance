from django.test import TestCase
from Search.models import Vehicle, Order
from SearchResults.views import StringSearch, FilterSearch, AvailabilitySearch



# Create your tests here.
class SearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Vehicle.objects.create(carmake="BMW", model="Super Model", series="Super Series", year=2018)
        Vehicle.objects.create(carmake="SAAB", model="Linear", series="Fusion", year=2020)
        Vehicle.objects.create(carmake="SAAB", model="BAAS", series="Unknown", year=2017)
        Order.objects.create(carid=Vehicle.objects.get(carmake="BMW"), createdate=20181023, pickupdate=20181023, returndate=20181025)

    def test_Empty_Search(self):
        self.assertIs(len(StringSearch("")), 0)

    def test_BMW_Search(self):
        self.assertEqual(StringSearch("BMW")[0], Vehicle.objects.get(carmake="BMW"))

    def test_Not_BMW(self):
        self.assertNotIn(Vehicle.objects.get(carmake="BMW"), StringSearch("SAAB"))

    def test_Filter_Empty(self):
        Filters = [0,0,0,0,0,0]
        List = []
        self.assertEqual(FilterSearch(List, Filters), [])

    def test_Filter_Single_Filter_Empty_List(self):
        Filters = [1,0,0,0,0,0]
        List = []
        self.assertIn(Vehicle.objects.get(carmake="BMW"), FilterSearch(List, Filters))

    def test_Filter_Remove_Items_that_dont_match_Filter(self):
        Filters = [1,0,0,0,0,0]
        List = []
        for i in Vehicle.objects.filter(carmake="SAAB"):
            List.append(i)
        self.assertNotIn(Vehicle.objects.filter(carmake="SAAB"), FilterSearch(List, Filters))

    def test_Availability_search_on_list_no_orders_between_dates(self):
        List = Vehicle.objects.all()
        self.assertEqual(list(Vehicle.objects.all()), list(AvailabilitySearch(List, 20070201, 20070205)))

    def test_Search_Between_Dates_Order_Exists(self):
        List = list(Vehicle.objects.all())
        self.assertNotIn(Vehicle.objects.get(carmake="BMW"), AvailabilitySearch(List, 20181023, 20181029))


