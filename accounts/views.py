from __future__ import unicode_literals

from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from django.db.models import Q
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from rest_framework import viewsets, filters

from transcribe.views import DefaultViewSetMixin

from .forms import AuthenticationForm, UserForm
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
    if request.method == 'POST':
        form = UserForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Changes saved successfully.")
    else:
        form = UserForm(instance=request.user)
    return render_to_response('accounts/account.html',
                              {'form': form},
                              context_instance=RequestContext(request))


@login_required
def password_saved(request):
    messages.success(request, 'Password Changed')
    return redirect('account')


class UserViewSet(DefaultViewSetMixin, viewsets.ModelViewSet):
    model = User
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name', '^email')
    queryset = User.objects.filter(is_active=True).all()
