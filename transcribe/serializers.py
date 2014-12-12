from rest_framework import serializers
from .models import Project, Item
from accounts.models import User


class ProjectSerializer(serializers.ModelSerializer):
    users = serializers.SlugRelatedField(many=True,
                                         slug_field='email',
                                         queryset=(User.objects
                                                   .filter(is_active=True)))

    class Meta:
        model = Project
        fields = ('id', 'name', 'owner', 'status', 'users')


class ItemSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(ItemSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = Item
        fields = ('id',
                  'name',
                  'type',
                  'source_type',
                  'url',
                  'project',
                  'owner',
                  'order',
                  )
