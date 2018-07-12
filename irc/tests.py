"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from .models import Irc, MSG_TYPES

MSG_TYPES_STANDARD = (
    ('M', 'Message'),
    ('PM', 'Private Message'),
    ('P', 'Part'),
    ('J', 'Join'),
    ('T', 'Topic'),
    ('E', 'Error'),
    ('N', 'Nick'),
    ('Q', 'Quit'),
    ('O', 'Other'),
)

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
        response = self.client.get('/irc/')
        self.assertContains(response, '<input type="password" name="word" placeholder="Enter the magic word.">')

    def test_login_reloads_correctly(self):
        """
        Tests that the login page reloads correctly when entering
        the wrong password
        """
        response = self.client.post('/irc/', {'word': 'wrongpass'})
        response = self.client.get('/irc/')
        self.assertContains(response, '<input type="password" name="word" placeholder="Enter the magic word.">')


class IrcFixturesTests(TestCase):
    fixtures = ['messages.json']

    def test_unicode_method(self):
        """
        Tests if the __unicode__ method in class Irc works as intended
        """
        instance = Irc.objects.get(pk=1)
        time = str(instance.time) + " " + instance.raw
        self.assertEquals(instance.__unicode__(), time)

    def test_nick_time_label(self):
        """
        Tests that nickname and time are correctly labled.
        """
        nick_label = Irc._meta.get_field('nick').verbose_name
        self.assertEquals(nick_label,'nick')
        time_label = Irc._meta.get_field('time').verbose_name
        self.assertEquals(time_label,'time')

    def test_nick_type_maxlen(self):
        """
        Tests that the size of the character field of nickname and 
        message type is correct.
        """
        message = Irc.objects.get(pk=3)
        nick_maxlen = message._meta.get_field('nick').max_length
        self.assertEquals(nick_maxlen,  255)
        type_maxlen = message._meta.get_field('msg_type').max_length
        self.assertEquals(type_maxlen, 3)

    def test_msg_types_changed(self):
        """
        Tests that no message types have changed
        """
        self.assertTrue(MSG_TYPES == MSG_TYPES_STANDARD)