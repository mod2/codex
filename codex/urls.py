from django.conf.urls import patterns, include, url
from django.contrib import admin
from transcribe.urls import router

urlpatterns = patterns(
    '',
    url(r'^$', 'codex.views.home', name='home'),
    url(r'^account/', include('accounts.urls', namespace='accounts')),
    url(r'^account/', 'accounts.views.account', name='account'),
    url(r'^admin/login/$', 'accounts.views.login', name='admin:login'),
    url(r'^admin/logout/$', 'accounts.views.logout', name='admin:logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^new-project/', 'transcribe.views.new_project', name='new_project'),
    url(r'^project/(.+?)/', 'transcribe.views.project', name='project'),
    url(r'^projects/', 'transcribe.views.all_projects', name='all_projects'),
    # url(r'^invites/', include('inviter2.urls', namespace='inviter2')),
)

transcribepatterns = patterns(
    '',
    url(r'^transcribe/api/', include(router.urls)),
    url(r'^transcribe/api-auth/', include('rest_framework.urls',
                                          namespace='rest_framework')),
)

urlpatterns += transcribepatterns
