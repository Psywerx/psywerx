from django.db import models

PROJECT_STATUS = (
    ('D', 'Development'),
    ('L', 'Live'),
    ('B', 'Beta'),
    ('A', 'Abandoned'),
)

MSG_TYPES = (
    ('M', 'Message'),
    ('PM', 'Private Message'),
    ('A', 'Action'),
    ('P', 'Part'),
    ('J', 'Join'),
    ('T', 'Topic'),
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
    nick = models.CharField(max_length = 255)
    name = models.CharField(max_length = 255, blank = True)
    address = models.CharField(max_length = 1000)
    msg_type = models.CharField(max_length = 3, choices = MSG_TYPES)
    message = models.TextField()
