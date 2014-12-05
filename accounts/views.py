from __future__ import unicode_literals

from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from rest_framework import viewsets

from transcribe.views import DefaultViewSetMixin

from .forms import AuthenticationForm
from .models import User
from .serializers import UserSerializer


def login(request):
    """Custom login view to login using an email address."""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(email=request.POST['email'],
                                password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    return redirect(request.POST.get('next', '/'))
    else:  # not a POST
        form = AuthenticationForm()
        form.next_url = request.GET.get('next', '/')
    return render_to_response('accounts/login.html',
                              {'form': form},
                              context_instance=RequestContext(request))


def logout(request):
    """Custom logout view to display a logged out page."""
    # TODO: add message that they have been successfully logged out and redirect
    # to the login page
    django_logout(request)
    return redirect('accounts:login')


@login_required
def account(request):
    return render_to_response('account.html')


class UserViewSet(DefaultViewSetMixin, viewsets.ModelViewSet):
    model = User
    serializer_class = UserSerializer

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        queryset = User.objects.filter(is_active=True)
        if query:
            queryset = queryset.filter(
                Q(name__startswith=query) | Q(email__startswith=query))
        return queryset
