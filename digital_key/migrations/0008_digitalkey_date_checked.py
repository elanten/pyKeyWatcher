# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-17 08:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digital_key', '0007_digitalkey_cert_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='digitalkey',
            name='date_checked',
            field=models.DateField(blank=True, null=True),
        ),
    ]
