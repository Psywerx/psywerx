'''
Created on Mar 1, 2011

@author: smotko
'''



def settings(request):
    from web.models import Static
    s = Static.objects.all()[0]
    return {'settings': s}
