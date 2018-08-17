from django.shortcuts import render_to_response
from django.template import RequestContext


def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))

def error500(request, template_name = '500.html'):
    return render_to_response(template_name, context_instance=RequestContext(request))  # pragma: no cover 

def error404(request, template_name = '404.html'):
    return render_to_response(template_name, context_instance=RequestContext(request))
