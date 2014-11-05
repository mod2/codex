from rest_framework import viewsets, authentication, permissions
from .models import Project
from .serializers import ProjectSerializer
from accounts.backends import EmailAuthAPIBackend


class DefaultViewSetMixin(object):
    authentication_classes = (
        EmailAuthAPIBackend,
        authentication.TokenAuthentication,
    )
    permission_classes = (
        permissions.IsAuthenticated,
    )
    paginate_by = None


class ProjectViewSet(DefaultViewSetMixin, viewsets.ModelViewSet):
    model = Project
    serializer_class = ProjectSerializer

    def get_queryset(self):
        if self.request.user:
            return Project.objects.filter(owner=self.request.user)
        else:
            return Project.objects.all()
