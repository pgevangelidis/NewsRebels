# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-20 12:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rebels', '0004_rss_date_rss'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='article',
            new_name='articleId',
        ),
    ]
