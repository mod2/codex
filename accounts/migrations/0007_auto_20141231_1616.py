# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_update_defaults'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 31, 16, 16, 38, 655747, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='layout',
            field=models.CharField(default='side_by_side', max_length=12, choices=[('side_by_side', 'Side By Side'), ('stacked', 'Stacked')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='theme',
            field=models.CharField(default='light', max_length=5, choices=[('light', 'Light'), ('dark', 'Dark')]),
            preserve_default=True,
        ),
    ]
