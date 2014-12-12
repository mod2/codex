from django.db import models
from accounts.models import User
from model_utils.models import StatusModel
from model_utils import Choices


class Project(StatusModel):
    STATUS = Choices('active', 'finished', 'inactive')
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name='projects')
    users = models.ManyToManyField(User, related_name="perm_projects",
                                   blank=True)

    def __unicode__(self):
        return self.name

    def get_next_item(self, user):
        rtn_item = None
        items = self.items.filter(owner=None)
        for item in items:
            if not item.is_skipped(user):
                item.owner = user
                item.save()
                rtn_item = item
                break
        return rtn_item

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
    owner = models.ForeignKey(User, related_name="owned_items", default=None,
                              blank=True, null=True)
    order = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return "{item} in project {project}".format(project=self.project,
                                                    item=self.name)

    @property
    def status(self):
        return self.transcripts.first().status

    def skip(self):
        skipped = Transcript(owner=self.owner, item=self,
                             status=Transcript.STATUS.skipped)
        skipped.save()
        self.owner = None
        self.save()

    def is_skipped(self, user):
        return self.transcripts.filter(owner=user, status='skipped').exists()

    class Meta:
        ordering = ['order', 'name']


class Transcript(StatusModel):
    STATUS = Choices('draft', 'finished', 'skipped')
    text = models.TextField()
    owner = models.ForeignKey(User, related_name='transcripts')
    date = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item, related_name='transcripts')

    def __unicode__(self):
        return "transcript by {owner} for item {item}".format(owner=self.owner,
                                                              item=self)

    class Meta:
        ordering = ['-date']
