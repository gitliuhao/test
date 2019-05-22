# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that openid already exists.'}, max_length=64, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9_]+$', 'Enter a valid openid. This value may contain only letters, numbers and underlined characters.', 'invalid')], help_text='Required. 64 characters or fewer. Letters, digits and underlined only.', unique=True, verbose_name='username')),
                ('nickname', models.CharField(help_text='Required. 64 characters or fewer.', max_length=64, verbose_name='nick name', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='UserProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(help_text='Required. 64 characters or fewer. Letters, digits and underlined only.', max_length=64, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9_]+$', 'Enter a valid key. This value may contain only letters, numbers and underlined characters.', 'invalid')])),
                ('value', models.TextField()),
                ('user', models.ForeignKey(related_name='properties', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'account_user_property',
                'verbose_name': 'user property',
                'verbose_name_plural': 'user properties',
            },
        ),
        migrations.AlterUniqueTogether(
            name='userproperty',
            unique_together=set([('user', 'key')]),
        ),
    ]
