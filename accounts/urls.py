from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter

from .views import UserViewSet

router = SimpleRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^login/$', 'accounts.views.login', name='login'),
    url(r'^logout/$', 'accounts.views.logout', name='logout'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='accounts_rest_framework'))
]
