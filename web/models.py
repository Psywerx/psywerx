from django.db import models
from django.template.defaultfilters import default
import re

PROJECT_STATUS = (
    ('D', 'Development'),
    ('L', 'Live'),
    ('B', 'Beta'),
    ('A', 'Abandoned'),
)

ACTION_START = u"\u0001" + "ACTION"
ACTION_END   = u"\u0001"

MSG_TYPES = (
    ('M', 'Message'),
    ('PM', 'Private Message'),
    ('P', 'Part'),
    ('J', 'Join'),
    ('T', 'Topic'),
    ('E', 'Error'),
    ('N', 'Nick'),
    ('Q', 'Quit'),
    # slap ???
    ('O', 'Other'),
)

class Language(models.Model):
    name = models.CharField(max_length = 255)
    
    def __unicode__(self):
        return self.name

class Framework(models.Model):
    name = models.CharField(max_length = 255)
    language = models.ForeignKey(Language)
    
    def __unicode__(self):
        return self.name
    
class Project(models.Model):
    name = models.CharField(max_length = 255)
    link = models.CharField(max_length = 255)
    description = models.TextField()
    status = models.CharField(max_length = 3, choices = PROJECT_STATUS)
    framework = models.ManyToManyField(Framework, blank = True)
    
    def __unicode__(self):
        return self.name
    
class Member(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField()
    website = models.CharField(max_length = 255, blank = True)
    twitter = models.CharField(max_length = 255, blank = True)
    facebook = models.CharField(max_length = 255, blank = True)
    github = models.CharField(max_length = 255, blank = True)
    linkedin = models.CharField(max_length = 255, blank = True)
    googleprofile = models.CharField(max_length = 255, blank = True)
        
    def __unicode__(self):
        return self.name
    
class Static(models.Model):
    title = models.CharField(max_length = 255)
    description = models.TextField()
    footer = models.CharField(max_length = 255)
        
    def __unicode__(self):
        return self.title
    
class Irc(models.Model):
    raw = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    nick = models.CharField(max_length = 255, blank = True)
    name = models.CharField(max_length = 255, blank = True)
    address = models.CharField(max_length = 1000, blank = True)
    msg_type = models.CharField(max_length = 3, choices = MSG_TYPES)
    msg_action = models.BooleanField(default = False)
    message = models.TextField(blank = True)
    
    def __unicode__(self):
        return str(self.time) + " " + self.raw 
        
    def parse(self, s):
        self.raw = s
        if s.startswith('ERROR'):
            self.msg_type = 'E'
        else:
            s = s.split(' ', 2)
            
            # process the user part:
            user = s[0].split('@')
            self.address = user[1]
            user = user[0].split('!')
            self.nick = user[0][1:]
            self.name = user[1]

            # process messages
            if s[1] == 'PRIVMSG':
                msg = s[2].split(' :', 1)
                if msg[0][:1] == '#':
                    self.msg_type = 'M'
                else:
                    self.msg_type = 'PM'                    
                self.message = msg[1]
                
               
                # check for ACTION:
                if self.message.startswith(ACTION_START) and self.message.endswith(ACTION_END):
                    self.message = self.message[8:]
                    self.msg_action = True
                
            elif s[1] == 'TOPIC':
                self.msg_type = 'T'
                self.message = s[2].split(' :',1)[1]
                
            # process events:
            elif s[1] in ('PART', 'QUIT', 'JOIN', 'NICK'):
                self.msg_type = s[1][:1]
                self.message = s[2][1:]            

            self.save() 
            
            # Add links:
            
            links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', self.message)
            for l in links:
                L = Link()
                L.link = l
                L.irc = self
                L.save()                   

        return s
    
class Link(models.Model):
    link = models.CharField(max_length = 1000)
    irc = models.ForeignKey(Irc)
    
    def __unicode__(self):
        return self.link
