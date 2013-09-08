from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^karma_stats', 'irc.views.karma_stats'),
    (r'^karma_nick', 'irc.views.karma_nick'),
    (r'^karma', 'irc.views.karma_add'),
    (r'^dump', 'irc.views.dump'),
    (r'^add', 'irc.views.irc_bot_add'),
    (r'^mygroups', 'irc.views.mygroups'),
    (r'^groups', 'irc.views.groups'),
    (r'^join', 'irc.views.join'),
    (r'^mention', 'irc.views.mention'),
    (r'^leaveAll', 'irc.views.leaveAll'),
    (r'^leave', 'irc.views.leave'),
    (r'^(\d+)/(\d+)/$', 'irc.views.irc'),
    (r'^$', 'irc.views.irc'),
)