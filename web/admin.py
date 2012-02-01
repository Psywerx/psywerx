from django.contrib import admin
from web.models import Project, Framework, Language, Member, Static, Irc, Link, Repost

admin.site.register(Project)
admin.site.register(Framework)
admin.site.register(Language)
admin.site.register(Member)
admin.site.register(Static)
admin.site.register(Irc)
admin.site.register(Link)
admin.site.register(Repost)