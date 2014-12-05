from rest_framework import serializers
from .models import Project
from accounts.models import User


class ProjectSerializer(serializers.ModelSerializer):
    users = serializers.SlugRelatedField(many=True,
                                         slug_field='email',
                                         queryset=(User.objects
                                                   .filter(is_active=True)))

    class Meta:
        model = Project
        fields = ('id', 'name', 'owner', 'status', 'users')
