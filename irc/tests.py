"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from mock import patch 
from .models import *
import hashlib

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

    @patch('irc.views.MAGIC_WORD', hashlib.sha224('root').hexdigest())
    def test_login(self):
        """
        Tests that logging in gives you a cookie
        """
        response = self.client.post('/irc/', {'word': 'root'})
        self.assertTrue(response.cookies['irctoken'])
        response = self.client.get('/irc/')
        self.assertContains(response, '<a href="/irc/dump_karma">Dump Karma</a>')
        self.assertContains(response, '<h4>This month:</h4>')

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

    def test_parse_method(self):
        """
        Tests every if/else statement in class Irc, method parse(see comments)
        """
        instance = Irc()
        channel = 'channel'
        char = '#'
        response = 'OK'

        # Tests response if an error occurs
        raw = 'ERROR'
        self.assertEquals(instance.parse(raw, channel), response)

        # Tests response if message is private and has a # (msg_type = M)
        raw = ':nick!name@address PRIVMSG #test :Hello, world!'
        self.assertEquals(instance.parse(raw, channel), response)

        # Tests response if message is private(starts with PRIVMSG) and doesn't have a # (msg_type = PM) and
        # message starts with ACTION_START and message ends with ACTION_END
        raw = ':hello!sir@madam PRIVMSG test :{0}Hello, world!{1}'.format(ACTION_START, ACTION_END)
        self.assertEquals(instance.parse(raw, channel), response)

        # Tests response if message is a topic(start with TOPIC)
        raw = ':nick!name@address TOPIC #test :Hello, world!'
        self.assertEquals(instance.parse(raw, channel), response)

        # tests response if message is anything else that is valid(starts with 'PART', 'QUIT', 'JOIN' or 'NICK')
        raw = ':nick!name@address {0} #test :Hello, world!'.format('PART', 'QUIT', 'JOIN', 'NICK')
        self.assertEquals(instance.parse(raw, channel), response)

        #tests response if message has a link in it
        raw = ':nick!name@address TOPIC #test :https://www.youtube.com/'
        self.assertEquals(instance.parse(raw, channel), response)

        #tests response if message has two identical links in it
        raw = ':nick!name@address TOPIC #test :https://www.youtube.com/ https://www.youtube.com/'
        response = u'REPOST nick nick T 2'
        self.assertEquals(instance.parse(raw, channel), response)

class GroupMembersFixturesTests(TestCase):
    fixtures = ['messages.json']

    def test_unicode_method(self):
        """
        Tests if the __unicode__ method in class GroupMembers works as intended
        """
        instance = GroupMembers.objects.get(pk=10)
        data = instance.nick + " " + instance.group + " " + instance.channel + " "
        self.assertEquals(instance.__unicode__(), data)

    def test_join_method(self):
        """
        Tests the join method in GroupMembers: firstUser an empty object, function fills
        it with provided data, secondUser gets joined into the group
        """
        firstUser = GroupMembers()
        secondUser = GroupMembers.objects.get(pk=11)

        firstUser.join('newUser', 'newGroup', False, 'psywerx')
        secondUser.join(secondUser.nick, secondUser.group, secondUser.offline, secondUser.channel)