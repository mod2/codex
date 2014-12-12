from __future__ import unicode_literals

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',
                  'name',
                  'is_active',
                  'is_admin',
                  'layout',
                  'theme',
                  )
