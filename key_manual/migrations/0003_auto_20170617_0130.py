# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-16 22:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('key_manual', '0002_auto_20170614_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manual',
            name='path',
            field=models.FilePathField(blank=True, null=True, path='c:/temp', recursive=True),
        ),
    ]