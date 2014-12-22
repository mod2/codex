# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transcribe', '0002_item_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='audio_start',
            field=models.PositiveSmallIntegerField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='audio_stop',
            field=models.PositiveSmallIntegerField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
    ]
