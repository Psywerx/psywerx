"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
# from /psywerx : $ python manage.py test irc
from django.test import TestCase

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class IrcViewTests(TestCase):
    def test_login_loads_correctly(self):
        """
        Tests that the login page loads correctly
        """
        response = self.client.get(r'/irc/')
        self.assertEqual(response.status_code, 200)

    def test_irc_loads_correctly(self):
        """
        Tests that you can log in using the magic word and the main
        irc page will load
        """
        response = self.client.post('/irc/', {'word': 'root'})
        response = self.client.get('/irc/')
        self.assertEqual(response.status_code, 200)