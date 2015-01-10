# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('transcribe', '0005_auto_20141231_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transcript',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 10, 3, 0, 31, 882516, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
    ]
