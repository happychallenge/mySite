# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-13 14:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('records', '0003_auto_20170513_1408'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evidence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('url', models.URLField(blank=True, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('media', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='master.Media')),
            ],
        ),
        migrations.AddField(
            model_name='evidence',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.News'),
        ),
        migrations.AddField(
            model_name='evidence',
            name='personevent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.PersonEvent'),
        ),
    ]