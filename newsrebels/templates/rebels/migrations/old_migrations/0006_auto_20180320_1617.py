# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-20 15:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rebels', '0005_auto_20180320_1317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userrss',
            name='hasRSS',
        ),
        migrations.RemoveField(
            model_name='userrss',
            name='suggested',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='article_url',
            new_name='url',
        ),
        migrations.RemoveField(
            model_name='article',
            name='articleId',
        ),
        migrations.AddField(
            model_name='article',
            name='rates',
            field=models.ManyToManyField(through='rebels.Rank', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rss',
            name='UserRss',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='rank',
            name='articleId',
        ),
        migrations.AddField(
            model_name='rank',
            name='articleId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rebels.Article'),
        ),
        migrations.RemoveField(
            model_name='rank',
            name='userId',
        ),
        migrations.AddField(
            model_name='rank',
            name='userId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='UserRSS',
        ),
    ]
