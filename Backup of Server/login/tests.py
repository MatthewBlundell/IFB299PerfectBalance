from django.test import TestCase
from Search.models import test_User
# Create your tests here.

class LoginTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_User.objects.create(username='admin@admin.com', password='password', name='Tob T', authenticationlevel=1)

    def test_login_correct_details(self):
        username = 'admin@admin.com'
        password = 'password'
        self.assertEqual(LoginAttempt(username,password), True)

    def test_bad_login_details(self):
        username = 'notadmin@admin.com'
        password = 'password'
        self.assertNotEqual(LoginAttempt(username,password), True)

#attempts to find a user with the input username and password
def LoginAttempt(Username, Pass):
    try:
        Userobject = test_User.objects.get(username=Username)
        if (Userobject.password == Pass):
            return True
        else:
            return False
    except:
        return False