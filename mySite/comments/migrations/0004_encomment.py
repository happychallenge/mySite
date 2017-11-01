# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-01 12:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0032_auto_20171101_2056'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comments', '0003_auto_20170921_1052'),
    ]

    operations = [
        migrations.CreateModel(
            name='ENComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='records.Event')),
                ('news', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='records.News')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='comments.ENComment')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
