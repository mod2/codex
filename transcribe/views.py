from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.decorators import login_required
# from django.core import serializers
from django.db.models import Q
# from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from rest_framework import viewsets, authentication, permissions, status
from rest_framework.decorators import list_route
from rest_framework.response import Response
import json

from .models import Project, Item, Transcript
from .serializers import ProjectSerializer, ItemSerializer, TranscriptSerializer


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


class TranscriptViewSet(DefaultViewSetMixin, viewsets.ModelViewSet):
    model = Transcript
    serializer_class = TranscriptSerializer

    def get_queryset(self):
        return Transcript.objects.filter(item=self.kwargs['item_pk'])


class ItemViewSet(DefaultViewSetMixin, viewsets.ModelViewSet):
    model = Item
    serializer_class = ItemSerializer

    def get_queryset(self):
        return Item.objects.filter(project=self.kwargs['project_pk'])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA, many=True)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['post'])
    def update_order(self, request, project_pk=None):
        items = Item.objects.filter(pk__in=request.data.keys())
        for item in items:
            item.order = request.data[unicode(item.pk)]
            item.save()
        return Response({"success": True})


@login_required
def home(request):
    # Get all the user's projects (projects where user is owner or the user is
    # in the project users list
    projects = Project.objects.filter(Q(owner=request.user)
                                      | Q(users=request.user),
                                      status='active')

    # Get user's latest transcript for the item (don't try this at home, kids)
    def add_transcript(item, user):
        item.latest_transcript = item.latest_transcript(user)
        return item

    # Get the user's items
    items = Item.objects.filter(owner=request.user)
    items = [add_transcript(item, request.user)
             for item in items if item.status(request.user) in ['draft', '']]

    return render_to_response('index.html', {'projects': projects,
                                             'items': items,
                                             'request': request})


@login_required
def new_project(request):
    return render_to_response('edit_project.html',
                              {'request': request, 'type': 'new',
                               'title': 'New Project',
                               'integrations': settings.INTEGRATIONS})


@login_required
def edit_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)

        if project.owner == request.user:
            context = {'request': request, 'project': project, 'type': 'edit',
                       'title': 'Edit Project',
                       'integrations': settings.INTEGRATIONS}
            return render_to_response('edit_project.html', context)
        else:
            return render_to_response('error.html', {'type': 403})
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
                    .filter(Q(owner=request.user)
                            | Q(users=request.user))
                    .exclude(status='active'))
        return render_to_response('archived_projects.html',
                                  {'request': request, 'projects': projects})
    except:
        pass


@login_required
def archived_items(request):
    try:
        items = Item.objects.filter(owner=request.user)
        items = [item for item in items
                 if item.status(request.user) == 'finished']

        return render_to_response('archived_items.html',
                                  {'request': request, 'items': items})
    except:
        pass


@login_required
def transcribe_item(request, project_id, item_id, transcript_id=None):
    try:
        project = Project.objects.get(id=project_id)
        item = Item.objects.get(id=item_id)

        # Get the latest transcript for this item
        try:
            latest_transcript = item.latest_transcript()
            text = latest_transcript.text
        except:
            text = ''

        # Override with specified transcript
        if transcript_id is not None:
            try:
                transcript = Transcript.objects.get(id=transcript_id, item=item)
                text = transcript.text
            except:
                pass

        # Make sure they have access (owner or are in the project)
        if request.user == project.owner or request.user in project.users.all:
            return render_to_response('transcribe.html', {'request': request,
                                                          'project': project,
                                                          'item': item,
                                                          'text': text,
                                                          'type': 'transcribe'})
        else:
            return render_to_response('error.html', {'request': request,
                                                     'type': 403})
    except:
        pass


@login_required
def get_next_item(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    item = project.get_next_item(request.user)
    if item:
        return redirect(transcribe_item, project_id, item.pk)
    else:
        return render_to_response('error.html', {'request': request,
                                                 'type': 404})


@login_required
def download_project(request, project_id, download_type):
    project = Project.objects.get(id=project_id)

    if download_type == 'text':
        # For each item, get the last transcript
        final_transcript = []
        for item in project.items.all().order_by('order', 'id'):
            if item.latest_transcript():
                final_transcript.append(item.latest_transcript().text)
        return HttpResponse('\n---\n'.join(final_transcript))
    elif download_type == 'json':
        def get_transcript_dict(transcript):
            return {
                'status': transcript.status,
                'text': transcript.text,
                'owner': transcript.owner.get_full_name(),
                'date': transcript.date.strftime('%B %d, %Y'),
            }

        def get_item_dict(item):
            return {
                'name': item.name,
                'type': item.type,
                'source_type': item.source_type,
                'url': item.url,
                'owner': item.owner.id,
                'order': item.order,
                'transcripts': [get_transcript_dict(t)
                                for t in item.transcripts.all()],
            }

        data = {
            'project': {
                'id': project.id,
                'name': project.name,
                'owner': project.owner.id,
                'users': [u.get_full_name() for u in project.users.all()],
                'items': [get_item_dict(i) for i in project.items.all()],
            },
            'users': [{'id': u.id, 'name': u.name, 'email': u.email}
                      for u in set(list(project.users.all()).append(project.owner))],
        }

        return JsonResponse(json.dumps(data), safe=False)
    else:
        return render_to_response('error.html', {'request': request,
                                                 'type': 500})
