# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-19 22:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0009_auto_20170319_2109'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='category',
            new_name='categories',
        ),
    ]