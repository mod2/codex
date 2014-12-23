from django import forms
from .models import User
import logging

log = logging.getLogger(__name__)


class UserForm(forms.ModelForm):
    """
    Form for the user account information/preferences.
    """

    # Turn off the colon label_suffix
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(UserForm, self).__init__(*args, **kwargs)

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

    # Turn off the colon label_suffix
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['email', 'password', 'next']
