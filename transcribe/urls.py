from django.conf.urls import url, include
from rest_framework import routers
from .views import ProjectViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)

urlpatters = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framwork.urls', namespace='rest_framwork'))
]
