# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-07-22 09:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jenkins_a', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jenkinsconfig',
            name='nickname',
            field=models.CharField(default='', max_length=50, verbose_name='别名'),
            preserve_default=False,
        ),
    ]
