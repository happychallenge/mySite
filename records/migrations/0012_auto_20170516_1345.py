# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-16 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0011_auto_20170514_1119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='updated_date',
        ),
        migrations.RemoveField(
            model_name='person',
            name='updated_user',
        ),
        migrations.AlterField(
            model_name='person',
            name='jobs',
            field=models.ManyToManyField(blank=True, to='master.Job'),
        ),
    ]