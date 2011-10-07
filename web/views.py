from web.models import Project, Member
from django.shortcuts import render_to_response
from django.template import RequestContext


def index(request):
    p = Project.objects.all().order_by('id').reverse()
    m = Member.objects.all()
    
    return render_to_response('index.html',{'projects' : p, 'members' : m, }, context_instance=RequestContext(request))

def irc(request):
    
    return render_to_response('irc.html', {'hello': 'world',}, context_instance=RequestContext(request))

def error500(request, template_name = '500.html'):
    return render_to_response(template_name, context_instance=RequestContext(request))

def error404(request, template_name = '404.html'):
    return render_to_response(template_name, context_instance=RequestContext(request))