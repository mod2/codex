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


urlpatterns = patterns(
    '',
    url(r'^$', home, name='home'),
    url(r'^account/', include('accounts.urls', namespace='accounts')),
    url(r'^account/', 'account', name='account'),
    url(r'^admin/login/$', 'accounts.views.login', name='admin:login'),
    url(r'^admin/logout/$', 'accounts.views.logout', name='admin:logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^invites/', include('inviter2.urls', namespace='inviter2')),
)
