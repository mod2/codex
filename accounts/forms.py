from django import forms
from .models import User
import logging

log = logging.getLogger(__name__)


class AccountForm(forms.ModelForm):
    """
    Form for the user account information/preferences.
    """
    password1 = forms.CharField(widget=forms.widgets.PasswordInput,
                                label='Password')
    password2 = forms.CharField(widget=forms.widgets.PasswordInput,
                                label='Password (again)')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(AccountForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class AuthenticationForm(forms.Form):
    """
    Login form.
    """
    email = forms.EmailField(widget=forms.widgets.TextInput)
    password = forms.CharField(widget=forms.widgets.PasswordInput)
    next = forms.CharField()

    class Meta:
        fields = ['email', 'password', 'next']
