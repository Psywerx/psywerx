from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^add', 'irc.views.irc_bot_add'),
    (r'^(\d+)/(\d+)/$', 'irc.views.irc'),
    (r'^$', 'irc.views.irc'),
)