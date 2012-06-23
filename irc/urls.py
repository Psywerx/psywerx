from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^karma_stats', 'irc.views.karma_stats'),
    (r'^karma_nick', 'irc.views.karma_nick'),
    (r'^karma', 'irc.views.karma_add'),
    (r'^add', 'irc.views.irc_bot_add'),
    (r'^(\d+)/(\d+)/$', 'irc.views.irc'),
    (r'^$', 'irc.views.irc'),
)