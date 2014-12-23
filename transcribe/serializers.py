from rest_framework import serializers
from .models import Project, Item, Transcript
from accounts.models import User


class ProjectSerializer(serializers.ModelSerializer):
    users = serializers.SlugRelatedField(many=True,
                                         slug_field='email',
                                         queryset=(User.objects
                                                   .filter(is_active=True)))

    class Meta:
        model = Project
        fields = ('id', 'name', 'owner', 'status', 'users')


class UserProjectSerializer(serializers.Serializer):
    emails = serializers.ListField(child=serializers.EmailField())
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    def save(self):
        project = self.validated_data['project']
        for email in self.validated_data['emails']:
            user = User.create_new_user(email)
            project.users.add(user)
        for email in project.users.all().values('email'):
            email = email['email']
            if email not in self.validated_data['emails']:
                user = User.objects.get(email=email)
                project.users.remove(user)


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
                  'audio_start',
                  'audio_stop',
                  )


class TranscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcript
        fields = ('id',
                  'text',
                  'owner',
                  'item',
                  'status',
                  )
