from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

handler500 = 'web.views.error500'
handler404 = 'web.views.error404'

urlpatterns = patterns('',
                       
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
    (r'^admin/', include(admin.site.urls)),
    (r'^irc/add', 'web.views.irc_bot_add'),
    (r'^irc/', 'web.views.irc'),
    (r'^$', 'web.views.index'),
)
