# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('transcribe', '0003_audio_fields_added'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transcript',
            options={'ordering': ['-last_modified']},
        ),
        migrations.RenameField(
            model_name='transcript',
            old_name='date',
            new_name='created',
        ),
        migrations.AddField(
            model_name='transcript',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 23, 22, 20, 50, 829497, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
    ]
