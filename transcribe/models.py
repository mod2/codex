from __future__ import unicode_literals, division

from django.db import models
from model_utils.models import StatusModel
from model_utils import Choices

from accounts.models import User


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

    def items_left(self):
        """ Return number of items left (where last transcript != finished) """

        def check_status(item):
            t = item.latest_transcript()

            # No transcript or latest transcript's status != finished
            if not t or t.status != 'finished':
                return True

            # Finished, so don't include it
            return False

        return len(filter(check_status, self.items.all()))

    def percentage_done(self):
        """ Return percentage completion of project """

        num_items = len(self.items.all())
        num_completed = num_items - self.items_left()

        # Don't divide by 0
        if num_items > 0:
            return num_completed / num_items * 100.0
        else:
            return 0.0

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

    audio_start = models.PositiveSmallIntegerField(null=True, default=None,
                                                   blank=True)
    audio_stop = models.PositiveSmallIntegerField(null=True, default=None,
                                                  blank=True)

    def __unicode__(self):
        return "{item} in project {project}".format(project=self.project,
                                                    item=self.name)

    def latest_transcript(self, user=None):
        if user:
            return self.transcripts.filter(owner=user).first()
        else:
            return self.transcripts.first()

    def status(self, user):
        transcript = self.latest_transcript(user)

        return transcript.status if transcript else ''

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
                                                              item=self.item)

    class Meta:
        ordering = ['-date']
