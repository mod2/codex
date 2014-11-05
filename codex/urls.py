from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from transcribe.urls import router


@login_required
def home(request):
    # TODO: This should probably be in a codex.views file.
    from django.shortcuts import render_to_response
    return render_to_response('index.html')


@login_required
def account(request):
    # TODO: Shouldn't this be in the accounts apps views?
    from django.shortcuts import render_to_response
    return render_to_response('account.html')


@login_required
def new_project(request):
    # TODO: Shouldn't this be in the transcribe apps views?
    from django.shortcuts import render_to_response
    return render_to_response('new_project.html')


@login_required
def project(request, project):
    # TODO: Shouldn't this be in the transcribe apps views?
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
    url(r'^new-project/', new_project, name='new_project'),
    url(r'^project/(.+?)/', project, name='project'),
    # url(r'^invites/', include('inviter2.urls', namespace='inviter2')),
)

transcribepatterns = patterns(
    '',
    url(r'^transcribe/api/', include(router.urls)),
    url(r'^transcribe/api-auth/', include('rest_framework.urls',
                                          namespace='rest_framework')),
)

urlpatterns += transcribepatterns
