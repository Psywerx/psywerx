from web.models import Project, Member
from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    p = Project.objects.all().order_by('id').reverse()
    m = Member.objects.all()
    return render_to_response('index.html',{'projects' : p, 'members' : m, }, context_instance=RequestContext(request))