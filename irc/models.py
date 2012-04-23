from django.db import models
import re

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
        response = 'OK'
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
            
            links = re.findall(r"(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s'!()\[\]{};:'\".,<>?']))", self.message)
            for l in links:
                l = l[0]
                reposts = Link.objects.all().filter(link = l).order_by('id')
                if len(reposts) > 0:
                    R = Repost()
                    R.irc = self
                    R.irc_original = reposts[0].irc
                    R.save()

                    response = " ".join(["REPOST", self.nick, reposts[0].irc.nick, self.msg_type])
                L = Link()
                L.link = l
                L.irc = self
                L.save()        

        return response
    
    class Meta:
        db_table = 'web_irc'
    
class Link(models.Model):
    link = models.CharField(max_length = 1000)
    irc = models.ForeignKey(Irc)
    
    def __unicode__(self):
        return self.link
    
    class Meta:
        db_table = 'web_link'
    
class Repost(models.Model):
    irc = models.ForeignKey(Irc, related_name='repost_irc')
    irc_original = models.ForeignKey(Irc, related_name='repost_irc_original')
    def __unicode__(self):
        return str(self.irc)
    
    class Meta:
        db_table = 'web_repost'
