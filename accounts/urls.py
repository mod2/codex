from __future__ import unicode_literals

from django.conf.urls import url, include
from django.contrib.auth.views import password_change
from rest_framework.routers import SimpleRouter

from .views import UserViewSet

router = SimpleRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^login/$', 'accounts.views.login', name='login'),
    url(r'^logout/$', 'accounts.views.logout', name='logout'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='accounts_rest_framework')),
    url(r'^password/saved/$', 'accounts.views.password_saved',
        name='password_saved'),
    url(r'^password/change/$', password_change,
        {'template_name': 'accounts/change_password.html',
         'post_change_redirect': 'accounts:password_saved'},
        name='password_change'),
]
