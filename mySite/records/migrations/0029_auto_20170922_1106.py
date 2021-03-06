# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-22 11:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nickname', '0002_auto_20170922_1106'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('records', '0028_auto_20170920_0700'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonNick',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('nickname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nickname.Nickname')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.Person')),
                ('user_hate', models.ManyToManyField(blank=True, related_name='nickname_hated', to=settings.AUTH_USER_MODEL)),
                ('user_like', models.ManyToManyField(blank=True, related_name='nickname_liked', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='personnick',
            unique_together=set([('person', 'nickname')]),
        ),
    ]
