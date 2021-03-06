# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-25 07:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0014_auto_20170509_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='attachment_description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='attachment',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='post',
            name='date_pub',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 25, 7, 16, 7, 127477)),
        ),
    ]
