from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^$', 'transcribe.views.home', name='home'),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^account/$', 'accounts.views.account', name='account'),
    url(r'^admin/login/$', 'accounts.views.login', name='admin:login'),
    url(r'^admin/logout/$', 'accounts.views.logout', name='admin:logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^new-project/$', 'transcribe.views.new_project', name='new_project'),
    url(r'^projects/(?P<project_id>\d+)/edit/$', 'transcribe.views.edit_project', name='edit_project'),
    url(r'^projects/(?P<project_id>\d+)/items/(?P<item_id>\d+)/$', 'transcribe.views.transcribe_item', name='transcribe_item'),
    url(r'^projects/(?P<project_id>\d+)/review/$', 'transcribe.views.review_project', name='review_project'),
    url(r'^projects/(?P<project_id>\d+)/get-next-item/$', 'transcribe.views.get_next_item', name='get_next_item'),
    url(r'^archived/$', 'transcribe.views.archived_projects', name='archived_projects'),
    url(r'^projects/(?P<project_id>\d+)/$', 'transcribe.views.project', name='project'),
    url(r'^transcribe/', include('transcribe.urls', namespace='transcribe')),
)
