# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('type', models.CharField(max_length=5, choices=[(b'image', b'image'), (b'audio', b'audio'), (b'video', b'video')])),
                ('source_type', models.CharField(max_length=7, choices=[(b'local', b'local'), (b'flickr', b'flickr'), (b'dropbox', b'dropbox'), (b'youtube', b'youtube')])),
                ('url', models.URLField()),
                ('order', models.PositiveSmallIntegerField()),
            ],
            options={
                'ordering': ['order', 'name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', model_utils.fields.StatusField(default=b'active', max_length=100, verbose_name='status', no_check_for_status=True, choices=[(b'active', b'active'), (b'finished', b'finished')])),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, verbose_name='status changed', monitor='status')),
                ('name', models.CharField(max_length=255)),
                ('owner', models.ForeignKey(related_name='projects', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='perm_projects', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transcript',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', model_utils.fields.StatusField(default=b'draft', max_length=100, verbose_name='status', no_check_for_status=True, choices=[(b'draft', b'draft'), (b'finished', b'finished')])),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, verbose_name='status changed', monitor='status')),
                ('text', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(related_name='transcripts', to='transcribe.Item')),
                ('owner', models.ForeignKey(related_name='transcripts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='item',
            name='project',
            field=models.ForeignKey(related_name='items', to='transcribe.Project'),
            preserve_default=True,
        ),
    ]
