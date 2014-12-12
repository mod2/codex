# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20141205_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='layout',
            field=models.CharField(default='side_by_side', max_length=12, choices=[('side_by_side', 'side_by_side'), ('stacked', 'stacked')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='theme',
            field=models.CharField(default='light', max_length=5, choices=[('light', 'light'), ('dark', 'dark')]),
            preserve_default=True,
        ),
    ]
