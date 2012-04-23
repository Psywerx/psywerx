from django.db import models
from django.template.defaultfilters import default
import re

PROJECT_STATUS = (
    ('D', 'Development'),
    ('L', 'Live'),
    ('B', 'Beta'),
    ('A', 'Abandoned'),
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
    
