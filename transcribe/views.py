from rest_framework import viewsets, authentication, permissions
from .models import Project
from .serializers import ProjectSerializer
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


class DefaultViewSetMixin(object):
    authentication_classes = (
        authentication.SessionAuthentication,
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


@login_required
def new_project(request):
    return render_to_response('new_project.html', { 'request': request })


@login_required
def project(request, project):
    return render_to_response('project.html', { 'request': request })
