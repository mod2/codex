from django.conf.urls import url, include, patterns
from rest_framework import routers
from .views import ProjectViewSet

router = routers.SimpleRouter()
router.register(r'projects', ProjectViewSet)

urlpatters = patterns(
    '',
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
)
