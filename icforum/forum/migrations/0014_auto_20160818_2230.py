# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-18 22:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0013_auto_20160816_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(upload_to='avatars/', verbose_name='Avatar'),
        ),
    ]
