# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-11-17 15:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('evento', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='organizador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.ProfileUser'),
        ),
    ]
