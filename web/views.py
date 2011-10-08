from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from web.models import Project, Member


def index(request):
    p = Project.objects.all().order_by('id').reverse()
    m = Member.objects.all()
    
    return render_to_response('index.html',{'projects' : p, 'members' : m, }, context_instance=RequestContext(request))

@csrf_exempt
def irc(request):
    
    if request.POST:
        print request.POST['raw']        
        
        
        return HttpResponse('OK')
    DEBUG = [
     ':smotko!~smotko@cpe-212-85-162-22.cable.telemach.net PRIVMSG #smotko-testing :hi thair!',
     ':smotko!~smotko@cpe-212-85-162-22.cable.telemach.net PART #smotko-testing',
     ':smotko!~smotko@cpe-212-85-162-22.cable.telemach.net JOIN #smotko-testing',
     ':smotko!~smotko@cpe-212-85-162-22.cable.telemach.net TOPIC #smotko-testing :hello world',
     'ERROR :Closing Link: cpe-212-85-162-22.cable.telemach.net (Ping timeout: 248 seconds)',
     ':smotko-neki!~smotko@cpe-212-85-162-22.cable.telemach.net NICK :smotko',
     ':smotko!~smotko@cpe-212-85-162-22.cable.telemach.net PRIVMSG botko123 :privat',
     ':smotko!~smotko@cpe-212-85-162-22.cable.telemach.net PRIVMSG botko123 :ACTION pek'

    ]

    debug = DEBUG[0].split(' ', 3)
    return render_to_response('irc.html', {'hello': debug,}, context_instance=RequestContext(request))

def error500(request, template_name = '500.html'):
    return render_to_response(template_name, context_instance=RequestContext(request))

def error404(request, template_name = '404.html'):
    return render_to_response(template_name, context_instance=RequestContext(request))