from web.models import Project, Member, Static
from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    p = Project.objects.all()
    m = Member.objects.all()
    s = Static.objects.all()[0]
    return render_to_response('index.html',{'projects' : p, 'members' : m, 'static' : s}, context_instance=RequestContext(request))