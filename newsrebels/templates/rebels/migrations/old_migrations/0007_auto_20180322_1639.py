# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-22 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rebels', '0006_auto_20180320_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='first',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last',
            field=models.CharField(max_length=128, null=True),
        ),
    ]