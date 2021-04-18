# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-10-24 17:02
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voyage', '0009_auto_20170705_1600'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkedVoyages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.IntegerField()),
                ('first', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='voyage.Voyage')),
                ('second', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='voyage.Voyage')),
            ],
        ),
    ]
