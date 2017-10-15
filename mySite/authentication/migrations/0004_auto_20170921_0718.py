# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-21 07:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20170810_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(upload_to='user_profile/%Y/%m/', verbose_name=''),
        ),
    ]