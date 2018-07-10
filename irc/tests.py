"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
# $ python manage.py dumpdata irc.Irc --format json --indent 4 > irc/fixtures/messages.json
# $ python manage.py loaddata irc/fixtures/messages.json

from django.test import TestCase
from .models import Irc, MSG_TYPES

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
        response = self.client.post('/irc/', {'word': 'root'}, follow = True)
        self.assertEqual(response.status_code, 200)


class IrcFixturesTests(TestCase):
    fixtures = ['messages.json']

    def test_unicode_method(self):
        """
        Tests if the __unicode__ method in class Irc works as intended
        """
        instance = Irc.objects.get(pk=1)
        time = str(instance.time) + " " + instance.raw
        self.assertEquals(instance.__unicode__(), time)

    def test_parse_metod(self):
        pass

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

    def test_no_blank(self):
        pass

    def test_msg_types_changed(self):
        """
        Tests that no message types have changed
        """
        messages_changed = True
        if MSG_TYPES == MSG_TYPES_STANDARD:
            messages_changed = False
        self.assertFalse(messages_changed)


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

"""
    def test_public_message(self):
        public_m = Irc.objects.get(pk=1)
        print(public_m.__unicode__)
        print(public_m.time)
        self.assertEquals(public_m.message, 'testing private')
        self.assertEquals(public_m.msg_type, 'PM')
"""


