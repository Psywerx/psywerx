from django.db import models

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
    language = models.OneToOneField(Language)
    
    def __unicode__(self):
        return self.name
    
class Project(models.Model):
    name = models.CharField(max_length = 255)
    link = models.CharField(max_length = 255)
    description = models.TextField()
    status = models.CharField(max_length = 3, choices = PROJECT_STATUS)
    framework = models.ForeignKey(Framework)
    
    def __unicode__(self):
        return self.name

class MemberLink(models.Model):
    name = models.CharField(max_length = 255)
    url = models.CharField(max_length = 255)   
    
    def __unicode__(self):
        return self.name 
    
class Member(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField()
    Link = models.ManyToManyField(MemberLink)
    
    def __unicode__(self):
        return self.name
    
class Static(models.Model):
    title = models.CharField(max_length = 255)
    description = models.TextField()
    
    def __unicode__(self):
        return self.title
    
    
