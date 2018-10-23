from django.test import TestCase
from Search.models import User, Order, Vehicle
from django.test import Client

# Create your tests here.

class LoginTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='admin@admin.com', password='password', name='Tob T', authenticationlevel=1)
        User.objects.create(username='not@admin.com', password='password', name='Tob T', authenticationlevel=0)
        Vehicle.objects.create(carmake="BMW", model="Super Model", series="Super Series", year=2018)
        Vehicle.objects.create(carmake="SAAB", model="Linear", series="Fusion", year=2020)
        Vehicle.objects.create(carmake="SAAB", model="BAAS", series="Unknown", year=2017)
        Order.objects.create(carid=Vehicle.objects.get(carmake="BMW"), createdate=20070207, pickupdate=20070207, returndate=20070207
                             , userid=User.objects.get(username='admin@admin.com'))
        Order.objects.create(carid=Vehicle.objects.get(model="Linear"), createdate=20070207, pickupdate=20070207,
                             returndate=20070207, userid=User.objects.get(username='not@admin.com'))

    def test_check_report_context_week(self):
        self.client.post('/login/', {'action': 'login', 'email': 'admin@admin.com', 'password': 'password'})
        response = self.client.get('/Reporting/20070201/1/')
        #as both orders are in the first week we can confirm that its counting the correct amount of orders for the first week
        self.assertEqual(response.context['week1total'],2)

    def test_check_report_context_day(self):
        self.client.post('/login/', {'action': 'login', 'email': 'admin@admin.com', 'password': 'password'})
        response = self.client.get('/Reporting/20070201/1/')
        #as both orders are on the 7th day we can confirm that its counting the correct amount of orders for the seventh day
        self.assertEqual(response.context['day7'],2)

    def test_check_all_other_weeks(self):
        self.client.post('/login/', {'action': 'login', 'email': 'admin@admin.com', 'password': 'password'})
        response = self.client.get('/Reporting/20070201/1/')
        self.assertEqual(response.context['week2total'], 0)
        self.assertEqual(response.context['week3total'], 0)
        self.assertEqual(response.context['week4total'], 0)


    def test_check_all_other_days_of_first_week(self):
        self.client.post('/login/', {'action': 'login', 'email': 'admin@admin.com', 'password': 'password'})
        response = self.client.get('/Reporting/20070201/1/')
        self.assertEqual(response.context['day1'],0)
        self.assertEqual(response.context['day2'],0)
        self.assertEqual(response.context['day3'],0)
        self.assertEqual(response.context['day4'],0)
        self.assertEqual(response.context['day5'],0)
        self.assertEqual(response.context['day6'],0)
