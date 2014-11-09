from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from transcribe.models import Project

@login_required
def home(request):
    # Get all the user's projects
    projects = Project.objects.filter(owner=request.user)

    return render_to_response('index.html', { 'projects': projects })
