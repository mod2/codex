from django import forms
from .models import User
import logging

log = logging.getLogger(__name__)


class UserForm(forms.ModelForm):
    """
    Form for the user account information/preferences.
    """
    class Meta:
        model = User
        fields = ['email', 'name', 'layout', 'theme']
        readonly_fields = ['email']


class AuthenticationForm(forms.Form):
    """
    Login form.
    """
    email = forms.EmailField(widget=forms.widgets.TextInput)
    password = forms.CharField(widget=forms.widgets.PasswordInput)
    next = forms.CharField()

    class Meta:
        fields = ['email', 'password', 'next']
