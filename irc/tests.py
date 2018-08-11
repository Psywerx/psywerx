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

def send_wrong_request(self, path):
    """
    Tests that the method, the path of which is passed as a parameter to this function, responds with NO if:
    1) the http method is not POST
    2) the http method is POST, but TOKEN is not passed
    3) the http method is POST, but the passed TOKEN is wrong
    """
    url = "/irc/%s" %path

    response = self.client.get(url)
    self.assertContains(response, 'NO')

    response = self.client.post(url)
    self.assertContains(response, 'NO')

    response = self.client.post(url, {'token': 'wrongtoken'})
    self.assertContains(response, 'NO')

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
    def test_irc(self):
        """
        Tests that logging in gives you a cookie and loads the right page
        """
        response = self.client.post('/irc/', {'word': 'root'})
        self.assertTrue(response.cookies['irctoken'])
        response = self.client.get('/irc/')
        self.assertContains(response, '<a href="/irc/dump_karma">Dump Karma</a>')
        self.assertContains(response, '<h4>This month:</h4>')

    @patch('irc.views.TOKEN', 'enter')
    def test_irc_bot_add(self):
        """
        Tests that the irc_bot_add method responds with OK if the correct TOKEN is passed, along with channel and raw
        Also tests that the response is NO when we send wrong requests through the send_wrong_request function
        """
        response = self.client.post('/irc/add', {'token': 'enter', 'raw': ':nick!name@address PRIVMSG #test :Hello!', 'channel': '#psywerx'})
        self.assertContains(response, 'OK')

        send_wrong_request(self, 'add')

    @patch('irc.views.TOKEN', 'enter')
    def test_karma_add(self):
        """
        Tests that the karma_add method responds with OK if the correct TOKEN is passed, along with channel and nick
        Also tests that the response is NO when we send wrong requests through the send_wrong_request function
        """
        response = self.client.post('/irc/karma', {'token': 'enter', 'nick': 'nickname', 'channel': '#psywerx'})
        self.assertContains(response, 'OK')

        send_wrong_request(self, 'karma')

    @patch('irc.views.TOKEN', 'enter')
    def test_karma_nick(self):
        """
        Only runs through the method
        """
        #has nick
        self.client.post('/irc/karma_nick', {'token': 'enter', 'nick': 'name', 'channel': '#psywerx'})
        #doesn't have nick
        self.client.post('/irc/karma_nick', {'token': 'enter', 'channel': '#psywerx'})

        send_wrong_request(self, 'karma_nick')    

    @patch('irc.views.TOKEN', 'enter')
    def test_join(self):
        """
        Tests that the join method responds with ok if the correct TOKEN is passed, along with nick, group, offline and channel
        Also tests that the response is NO when we send wrong requests through the send_wrong_request function
        """
        response = self.client.post('/irc/join', {'token': 'enter', 'nick': 'name', 'group': 'Psywerx', 'offline': 'false', 'channel': '#psywerx'})
        self.assertContains(response, 'ok')

        send_wrong_request(self, 'join')

    @patch('irc.views.TOKEN', 'enter')
    def test_leave(self):
        """
        Tests that the leave method responds with ok if the correct TOKEN is passed, along with nick, group, offline and channel
        Also tests that the response is NO when we send wrong requests through the send_wrong_request function
        """
        response = self.client.post('/irc/leave', {'token': 'enter', 'nick': 'name', 'group': 'Psywerx', 'channel': '#psywerx'})
        self.assertContains(response, 'ok')

        send_wrong_request(self, 'leave')

class IrcModelsTests(TestCase):
    fixtures = ['messages.json']

    def test_unicode_methods(self):
        """
        Tests if the __unicode__ method in class Irc works as intended
        Tests if the __unicode__ method in class GroupMembers works as intended
        """
        instance = Irc.objects.get(pk=1)
        time = str(instance.time) + " " + instance.raw
        self.assertEquals(instance.__unicode__(), time)

        instance = GroupMembers.objects.get(pk=10)
        data = instance.nick + " " + instance.group + " " + instance.channel + " "
        self.assertEquals(instance.__unicode__(), data)

    def test_nick_time_label(self):
        """
        Tests that nickname and time are correctly labeled.
        """
        nick_label = Irc._meta.get_field('nick').verbose_name
        self.assertEquals(nick_label,'nick')
        time_label = Irc._meta.get_field('time').verbose_name
        self.assertEquals(time_label,'time')

    def test_nick_type_maxlen(self):
        """
        Tests that the size of the character field of nickname and 
        message type in the Irc class is correct.
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
        self.assertIn('https://www.youtube.com/', Link.objects.all().__str__())

    def test_join_leave_methods(self):
        """
        Tests the join and leave methods in class GroupMembers. First two users join and we check the parameters of the created object.
        Then one user leaves and we make sure that their object is deleted
        """
        instance = GroupMembers()
        first_user = GroupMembers.objects.get(pk=10)
        second_user = GroupMembers.objects.get(pk=11)

        instance.join(first_user.nick, first_user.group, first_user.offline, first_user.channel)
        instance.join(second_user.nick, second_user.group, second_user.offline, second_user.channel)

        group_members_objects = GroupMembers.objects.all()
        first_user_parameters = '{0} {1} {2}'.format(first_user.nick, first_user.group, first_user.channel)
        second_user_parameters = '{0} {1} {2}'.format(second_user.nick, second_user.group, second_user.channel)
        self.assertIn(first_user_parameters, group_members_objects.__str__())
        self.assertIn(second_user_parameters, group_members_objects.__str__())

        instance.leave(second_user.nick, second_user.group, second_user.channel)
        self.assertNotIn(second_user_parameters, group_members_objects.__str__())