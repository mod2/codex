from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'is_admin', 'is_active')

    def clean_password(self):
        return self.initial['password']


@admin.register(User)
class UserAdmin(UserAdmin):
    form = UserChangeForm

    list_display = ('email', 'name', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )

    search_fields = ('email', 'name')
    ordering = ('email',)
    filter_horizontal = ()

admin.site.unregister(Group)
