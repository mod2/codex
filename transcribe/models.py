from django.db import models
# from accounts.models import User
# from model_utils import StatusModel, Choices


# class Project(StatusModel):
#     STATUS = Choices('active', 'finished')
#     name = models.CharField(max_length=255)
#     owner = models.ForeignKey(User, related_name='projects')
#     users = models.ManyToManyField(User, related_name="perm_projects",
#                                    blank=True)

#     def __unicode__(self):
#         return self.name

#     class Meta:
#         ordering = ['name']
