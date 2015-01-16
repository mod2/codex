# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('transcribe', '0006_auto_20150110_0300'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectTranscript',
            fields=[
                ('transcript_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='transcribe.Transcript')),
                ('last_item_seen', models.ForeignKey(related_name='+', to='transcribe.Item')),
                ('project', models.ForeignKey(related_name='final_transcripts', to='transcribe.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=('transcribe.transcript',),
        ),
        migrations.AlterField(
            model_name='transcript',
            name='item',
            field=models.ForeignKey(related_name='transcripts', to='transcribe.Item', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transcript',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 16, 4, 2, 0, 28227, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
    ]
