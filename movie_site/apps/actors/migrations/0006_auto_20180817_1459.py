# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-17 14:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actors', '0005_auto_20180816_1446'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='actors',
        ),
        migrations.DeleteModel(
            name='Movie',
        ),
    ]
