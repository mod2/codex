from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth import authenticate
from .forms import AuthenticationForm


def login(request):
    """Custom login view to login using an email address."""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        print(request.POST)
        print(request.GET)
        if form.is_valid():
            user = authenticate(email=request.POST['email'],
                                password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    return redirect(request.POST.get('next', '/'))
    else:
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
