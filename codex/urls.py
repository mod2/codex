from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    from django.shortcuts import render_to_response
    return render_to_response('index.html')

@login_required
def account(request):
    from django.shortcuts import render_to_response
    return render_to_response('account.html')

@login_required
def new_project(request):
    from django.shortcuts import render_to_response
    return render_to_response('new_project.html')

@login_required
def project(request, project):
    from django.shortcuts import render_to_response
    return render_to_response('project.html')


urlpatterns = patterns(
    '',
    url(r'^$', home, name='home'),
    url(r'^account/', include('accounts.urls', namespace='accounts')),
    url(r'^account/', account, name='account'),
    url(r'^admin/login/$', 'accounts.views.login', name='admin:login'),
    url(r'^admin/logout/$', 'accounts.views.logout', name='admin:logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^invites/', include('inviter2.urls', namespace='inviter2')),
    url(r'^new-project/', new_project, name='new_project'),
    url(r'^project/(.+?)/', project, name='project'),
)
