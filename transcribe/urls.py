from __future__ import unicode_literals

from django.conf.urls import url, include, patterns
from rest_framework_nested import routers

from .views import ProjectViewSet, ItemViewSet, TranscriptViewSet

router = routers.SimpleRouter()
router.register(r'projects', ProjectViewSet)

projects_router = routers.NestedSimpleRouter(router, r'projects',
                                             lookup='project')
projects_router.register(r'items', ItemViewSet)

items_router = routers.NestedSimpleRouter(projects_router, r'items',
                                          lookup='item')
items_router.register(r'transcripts', TranscriptViewSet)

urlpatterns = patterns(
    '',
    url('^api/', include(router.urls)),
    url('^api/', include(projects_router.urls)),
    url('^api/', include(items_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
)
