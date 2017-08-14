# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-14 05:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('records', '0022_auto_20170813_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='event_follow', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='user_like',
            field=models.ManyToManyField(blank=True, related_name='event_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
