from django.db import models
from accounts.models import User
from model_utils.models import StatusModel
from model_utils import Choices


class Project(StatusModel):
    STATUS = Choices('active', 'finished')
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name='projects')
    users = models.ManyToManyField(User, related_name="perm_projects",
                                   blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Item(models.Model):
    TYPES = Choices('image', 'audio', 'video')
    SOURCES = Choices('local', 'flickr', 'dropbox', 'youtube')

    name = models.TextField()
    type = models.CharField(max_length=5, choices=TYPES)
    source_type = models.CharField(max_length=7, choices=SOURCES)
    url = models.URLField()
    project = models.ForeignKey(Project, related_name='items')
    order = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return "{item} in project {project}".format(project=self.project,
                                                    item=self.name)

    class Meta:
        ordering = ['order', 'name']


class Transcript(StatusModel):
    STATUS = Choices('draft', 'finished')
    text = models.TextField()
    owner = models.ForeignKey(User, related_name='transcripts')
    date = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item, related_name='transcripts')

    def __unicode__(self):
        return "transcript by {owner} for item {item}".format(owner=self.owner,
                                                              item=self)

    class Meta:
        ordering = ['-date']
