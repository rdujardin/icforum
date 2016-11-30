# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-28 21:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='notify',
            field=models.CharField(choices=[('notify_all', 'Notify every action on the forum'), ('notify_participated_topics_every_mail', 'Notify updates on participated topics and every mail'), ('notify_explicitly_chosen_topics_every_mail', 'Notify updates on explicitly chosen topics and every mail'), ('notify_nothing', 'Notify nothing')], default='notify_all', max_length=100),
        ),
    ]
