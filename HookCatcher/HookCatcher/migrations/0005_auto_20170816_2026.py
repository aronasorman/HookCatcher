# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-16 20:26
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HookCatcher', '0004_remove_pr_git_pr_commit'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now=True)),
                ('message', models.TextField()),
                ('is_error', models.BooleanField(default=False)),
                ('pr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HookCatcher.PR')),
            ],
        ),
        migrations.AddField(
            model_name='diff',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]