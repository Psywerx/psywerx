from django.core.paginator import Paginator
from django.db.models.aggregates import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from irc.models import Irc, Link, Karma
from datetime import date, timedelta
import hashlib
import json

TOKEN = '16edde56d1801c65ec96a4d607a67d89'

@csrf_exempt
def irc_bot_add(request):
    if request.POST:
        if request.POST["token"] == TOKEN:
            i = Irc()
            result = i.parse(request.POST['raw'], request.POST['channel'])
            return HttpResponse(result)
    return HttpResponse("NO")
    #return render_to_response('404.html', context_instance=RequestContext(request))
    
@csrf_exempt
def karma_add(request):
    if request.POST:
        if request.POST["token"] == TOKEN:
            k = Karma()
            k.nick = request.POST['nick']
            k.channel = request.POST['channel']
            print k.nick, k.channel
            k.save()
            return HttpResponse("OK")
    return HttpResponse("NO")

@csrf_exempt
def karma_nick(request):
    if request.POST:
        if request.POST["token"] == TOKEN:
            if "nick" in request.POST:
                karma = len(Karma.objects.filter(nick = request.POST['nick']))
            else:
                karma = json.dumps([o for o in Karma.objects.all().values('nick').annotate(karma=Count('nick')).order_by('-karma')[:5]])
            return HttpResponse(karma)
    return HttpResponse("NO")

def dump(request):
    out = [{"message": a.message, "time": str(a.time), "nick": a.nick, \
            "msg_type": a.msg_type, "msg_action": a.msg_action} for a in Irc.objects.all()]
    return HttpResponse(json.dumps(out), mimetype="application/json")

MAGIC_WORD = "6cf28bcedc3a628a4896817156e1ace5108ce6266a00fd556861d656"
COOKIE_TOKEN = "2d9aa7a812f458a8d278d35272c6dc28b03357b7db38e553ea98a7f0"
CHANNEL = "#psywerx"
def irc(request, page=1, link_page=1):
    
    # Set the cookie
    if request.POST:
        
        if request.POST.has_key('word') and hashlib.sha224(request.POST['word']).hexdigest() == MAGIC_WORD:
            r = HttpResponseRedirect('.')
            r.set_cookie("irctoken", COOKIE_TOKEN, 60*60*24*356*100)
            return r
            
    irc_token = request.COOKIES.get("irctoken", "")
    
    if irc_token == COOKIE_TOKEN:
        
        if request.POST.has_key('term'):
            q = Irc.objects.all().filter(message__icontains = request.POST['term'], channel__iexact = CHANNEL).order_by('time').reverse()
        else:
            q = Irc.objects.all().filter(channel__iexact = CHANNEL).order_by('time').reverse()
        
        p = Paginator(q, 100)
        
        links = Link.objects.all().filter(irc__channel=CHANNEL).order_by('id').reverse()
        links_p = Paginator(links, 10)

        # all time:
        karma = Karma.objects.all().filter(channel__iexact = CHANNEL).values('nick').annotate(karma=Count('nick')).order_by('-karma')[:5]
        
        # this week:
        week_start = date.today() - timedelta(days = date.today().weekday())
        karma_week = Karma.objects.filter(time__gte = week_start, channel__iexact = CHANNEL).values('nick').annotate(karma=Count('nick')).order_by('-karma')[:5]

        # this month:
        month_start = date.today() - timedelta(days = date.today().day-1)
        karma_month = Karma.objects.filter(time__gte = month_start, channel__iexact = CHANNEL).values('nick').annotate(karma=Count('nick')).order_by('-karma')[:5]

                
        return render_to_response('irc.html', {'log': p.page(page), 'links': links_p.page(link_page), 'karma':karma, 'karma_week':karma_week, 'karma_month':karma_month}, context_instance=RequestContext(request))
    else:
        return render_to_response('irc_access.html', {'hello': "aaa",}, context_instance=RequestContext(request))
