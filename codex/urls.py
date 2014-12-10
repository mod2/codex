from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^$', 'codex.views.home', name='home'),
    url(r'^account/', include('accounts.urls', namespace='accounts')),
    url(r'^account/', 'accounts.views.account', name='account'),
    url(r'^admin/login/$', 'accounts.views.login', name='admin:login'),
    url(r'^admin/logout/$', 'accounts.views.logout', name='admin:logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^new-project/', 'transcribe.views.new_project', name='new_project'),
    url(r'^project/(.+?)/edit/', 'transcribe.views.edit_project', name='edit_project'),
    url(r'^project/(.+?)/items/(.+?)/', 'transcribe.views.transcribe_item', name='transcribe_item'),
    url(r'^project/(.+?)/', 'transcribe.views.project', name='project'),
    url(r'^review/(.+?)/', 'transcribe.views.review_project', name='review_project'),
    url(r'^archived/', 'transcribe.views.archived_projects', name='archived_projects'),
    url(r'^transcribe/', include('transcribe.urls', namespace='transcribe')),
    # url(r'^invites/', include('inviter2.urls', namespace='inviter2')),
)

# transcribepatterns = patterns(
#     '',
#     url(r'^transcribe/api/', include(router.urls)),
#     url(r'^transcribe/api-auth/', include('rest_framework.urls',
#                                           namespace='rest_framework')),
# )

# urlpatterns += transcribepatterns
