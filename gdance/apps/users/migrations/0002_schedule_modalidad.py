# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-11-17 15:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='modalidad',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.Modalidad'),
            preserve_default=False,
        ),
    ]
