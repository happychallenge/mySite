# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-12 12:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0018_auto_20170812_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='tag',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
