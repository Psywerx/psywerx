from web.models import Project, Framework, Language
from django.contrib import admin
from django.db import transaction

admin.site.register(Project)
admin.site.register(Framework)
admin.site.register(Language)
