# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-26 09:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digital_key', '0003_auto_20170619_1152'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('link', models.URLField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='digitalkey',
            name='work_systems',
            field=models.ManyToManyField(to='digital_key.WorkSystem'),
        ),
    ]