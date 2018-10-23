from django.test import TestCase
from Search.models import User
# Create your tests here.

class LoginTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='admin@admin.com', password='password', name='Tob T', authenticationlevel=1)
        User.objects.create(username='not@admin.com', password='password', name='Tob T', authenticationlevel=0)

    def test_login_correct_details(self):
        self.client.post('/login/', {'action': 'login', 'email': 'admin@admin.com', 'password':'password'})
        #email only exists if a user successfully logged in
        self.assertEqual(self.client.session['email'], 'admin@admin.com')


    def test_bad_login_details(self):
        self.client.post('/login/', {'action': 'login', 'email': 'admin@admin.com', 'password':'no'})
        #session Login only exists when a user fails to log in
        self.assertEqual(self.client.session['Login'], 'Failed')

    def test_report_page_no_login(self):
        response = self.client.get('/Reporting/20070207/1/')
        self.assertNotEqual(response.status_code, 200)

    def test_report_page_login(self):
        self.client.post('/login/', {'action': 'login', 'email': 'admin@admin.com', 'password': 'password'})
        response = self.client.get('/Reporting/20070207/1/')
        self.assertEqual(response.status_code, 200)

    def test_report_page_login_non_admin(self):
        self.client.post('/login/', {'action': 'login', 'email': 'not@admin.com', 'password': 'password'})
        response = self.client.get('/Reporting/20070207/1/')
        self.assertNotEqual(response.status_code, 200)