# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-24 07:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('conditions', '0002_condpost_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='rulePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ruleId', models.IntegerField()),
                ('ruletext', models.CharField(max_length=200)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('audusr', models.CharField(max_length=10)),
                ('ruleInt', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='condpost',
            name='audusr',
            field=models.CharField(default='learners', max_length=10),
        ),
    ]
