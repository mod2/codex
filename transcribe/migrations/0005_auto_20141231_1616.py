# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('transcribe', '0004_auto_20141223_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transcript',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 31, 16, 16, 38, 661046, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
    ]
