from django.test import TestCase
from Search.models import Vehicle, Order, User, Store


# Create your tests here.
class RentingTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Store.objects.create(storeid=1, city='Darlinghurst')
        Vehicle.objects.create(carmake="BMW", model="Super Model", series="Super Series", year=2018, storeid=Store.objects.get(storeid=1))
        User.objects.create(username='admin@admin.com', password='password', name='Tob T', authenticationlevel=1)


    def test_rent_vehicle(self):
        self.assertEqual(len(Order.objects.all()), 0)
        session = self.client.session
        session['email'] = 'admin@admin.com'
        session.save()
        car = Vehicle.objects.get(carmake="BMW")
        address = '/Car_Information/'+ str(car.carid) +'/Rent/Rent/'
        response = self.client.post(address, {'endlocation':'Darlinghurst','pickupdate':'2018-10-23', 'returndate':'2018-10-24'})
        self.assertEqual(len(Order.objects.all()), 1)
