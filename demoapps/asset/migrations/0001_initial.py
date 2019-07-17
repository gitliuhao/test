# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-07-17 11:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=20, verbose_name='用户名')),
                ('host', models.CharField(blank=True, max_length=20, unique=True, verbose_name='主机ip')),
                ('ssh_secret_key', models.FileField(upload_to='ssh_key', verbose_name='ssh远程秘钥')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '主机',
                'verbose_name_plural': '主机列表',
            },
        ),
    ]
