from rest_framework import viewsets, authentication, permissions
from .models import Project, Item
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
        qs = Project.objects.exclude(status='inactive')
        if self.request.user:
            qs = qs.filter(owner=self.request.user)
        return qs


@login_required
def new_project(request):
    return render_to_response('edit_project.html', { 'request': request, 'type': 'new', 'title': 'New Project' })

@login_required
def edit_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        return render_to_response('edit_project.html', { 'request': request, 'project': project, 'type': 'edit', 'title': 'Edit Project' })
    except:
        pass

@login_required
def project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        return render_to_response('project.html', {'request': request,
                                                   'project': project})
    except:
        pass


@login_required
def review_project(request, project_id):
    """ View to show project items that need review. """
    try:
        project = Project.objects.get(id=project_id)
        return render_to_response('review_project.html', {'request': request,
                                                          'project': project})
    except:
        pass


@login_required
def archived_projects(request):
    try:
        projects = (Project.objects
                    .filter(owner=request.user)
                    .exclude(status='active'))
        return render_to_response('archived_projects.html',
                                  {'request': request, 'projects': projects})
    except:
        pass

@login_required
def transcribe_item(request, project_id, item_id):
    try:
        project = Project.objects.get(id=project_id)
        item = Item.objects.get(id=item_id)

        # Make sure they have access (owner or are in the project)
        if request.user == project.owner or request.user in project.users.all:
            return render_to_response('transcribe.html', {'request': request,
                                                        'project': project,
                                                        'item': item})
        else:
            return render_to_response('error.html', {'request': request,
                                                     'type': 403})
    except:
        pass
