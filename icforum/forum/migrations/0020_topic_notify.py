# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-28 21:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0019_auto_20161113_0058'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='notify',
            field=models.ManyToManyField(blank=True, related_name='followed_topics', to=settings.AUTH_USER_MODEL),
        ),
    ]
