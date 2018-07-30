"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from mock import patch 
from .models import *
from .views import *
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
        Tests that logging in gives you a cookie and loads the right page
        """
        response = self.client.post('/irc/', {'word': 'root'})
        self.assertTrue(response.cookies['irctoken'])
        response = self.client.get('/irc/')
        self.assertContains(response, '<a href="/irc/dump_karma">Dump Karma</a>')
        self.assertContains(response, '<h4>This month:</h4>')

    @patch('irc.views.MAGIC_WORD', hashlib.sha224('root').hexdigest())
    def test_irc_bot_add_nothing(self):
        """
        Tests that the irc_bot_add method responds with NO if no token is passed 
        """
        response = self.client.post('/irc/', {'word': 'root'})
        response = self.client.get('/irc/add')
        self.assertContains(response, 'NO')

    @patch('irc.views.MAGIC_WORD', hashlib.sha224('root').hexdigest())
    def test_irc_bot_add(self):
        """
        Tests that the irc_bot_add method responds with OK if the correct token TOKEN is passed 
        """
        response = self.client.post('/irc/add', {'raw': ':nick!name@address PRIVMSG #test :Hello!', 'channel': '#psywerx', 'token': '16edde56d1801c65ec96a4d607a67d89'})
        self.assertContains(response, 'OK')

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
        response = 'OK'

        # Tests response if an error occurs
        raw = 'ERROR'
        self.assertEquals(instance.parse(raw, channel), response)
        self.assertEquals(instance.msg_type, 'E')

        # Tests response if message is private and has a #channel
        # msg_type must be PM, msg_action must be false
        raw = ':nick!name@address PRIVMSG #test :Hello, world!'
        self.assertEquals(instance.parse(raw, channel), response)
        self.assertEquals(instance.msg_type, 'M')
        expected_message = raw.split(' ', 2)[2].split(' :', 1)[1]
        self.assertEquals(expected_message, instance.message)
        self.assertFalse(instance.msg_action)

        # Tests response if message is private(starts with PRIVMSG and doesn't have a channel name, preceeded by #), 
        # message starts after ACTION_START and ends before ACTION_END
        # msg_type must be M, msg_action must be true
        raw = ':hello!sir@madam PRIVMSG test :{0}Hello, world!{1}'.format(ACTION_START, ACTION_END)
        expected_message = raw.split(' ', 2)[2].split(' :', 1)[1][7:-1]
        self.assertEquals(instance.parse(raw, channel), response)
        self.assertEquals(instance.msg_type, 'PM')
        self.assertEquals(expected_message, instance.message)
        self.assertNotIn(ACTION_START, instance.message)
        self.assertTrue(instance.msg_action)

        # Tests response if message is a topic(start with TOPIC)
        # msg_type must be T, msg_action must be false
        raw = ':nick!name@address TOPIC #test :Hello, world!'
        self.assertEquals(instance.parse(raw, channel), response)
        expected_message = raw.split(' ', 2)[2].split(' :', 1)[1]
        self.assertEquals(expected_message, instance.message)
        self.assertEquals(instance.msg_type, 'T')
        self.assertFalse(instance.msg_action)

        # tests response if message is anything else that is valid(starts with 'PART', 'QUIT', 'JOIN' or 'NICK')
        # msg_type must be the first letter of the command name, msg_action must be false
        command_list = ('PART', 'QUIT', 'JOIN', 'NICK')
        for command in command_list:
            raw = ':nick!name@address {0} #test :Hello, world!'.format(command)
            self.assertEquals(instance.parse(raw, channel), response)
            self.assertEquals(instance.msg_type, command[0])
            self.assertFalse(instance.msg_action)

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
