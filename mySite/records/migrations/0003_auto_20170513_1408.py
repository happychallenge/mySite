# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-13 14:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0002_personevent_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evaluation',
            old_name='person_event',
            new_name='personevent',
        ),
    ]