# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-25 23:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('records', '0012_auto_20170516_1345'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.Event')),
            ],
        ),
        migrations.RemoveField(
            model_name='evidence',
            name='created_user',
        ),
        migrations.RemoveField(
            model_name='evidence',
            name='news',
        ),
        migrations.RemoveField(
            model_name='evidence',
            name='personevent',
        ),
        migrations.AlterField(
            model_name='news',
            name='url',
            field=models.URLField(blank=True, null=True, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='personevent',
            unique_together=set([('person', 'event')]),
        ),
        migrations.DeleteModel(
            name='Evidence',
        ),
        migrations.AddField(
            model_name='eventnews',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.News'),
        ),
        migrations.AlterUniqueTogether(
            name='eventnews',
            unique_together=set([('event', 'news')]),
        ),
    ]
