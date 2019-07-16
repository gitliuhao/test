# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-07-15 09:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('asset', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JenkinsConfig',
            fields=[
                ('asset_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='asset.Asset')),
                ('url', models.URLField(verbose_name='访问地址')),
            ],
            options={
                'verbose_name': 'jenkins配置',
            },
            bases=('asset.asset',),
        ),
    ]
