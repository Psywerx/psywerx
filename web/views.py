from web.models import Project
from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    p = Project.objects.all()
    return render_to_response('index.html',{'projects' : p}, context_instance=RequestContext(request))