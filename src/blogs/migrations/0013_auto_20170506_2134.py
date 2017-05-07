# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-06 21:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0012_auto_20170324_0325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='attachment_type',
            field=models.CharField(choices=[('V', 'Video'), ('I', 'Image'), ('N', 'None')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='post',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='blogs.Blog'),
        ),
        migrations.AlterField(
            model_name='post',
            name='date_pub',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 6, 21, 34, 30, 291100)),
        ),
    ]
