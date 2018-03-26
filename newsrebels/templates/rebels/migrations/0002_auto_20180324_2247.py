# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-24 20:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rebels', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='rss',
            name='is_deleted',
        ),
        migrations.AddField(
            model_name='articlerss',
            name='is_deleted',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='rank',
            name='is_deleted',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='userrss',
            name='is_deleted',
            field=models.IntegerField(default=1),
        ),
    ]