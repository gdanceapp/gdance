# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-10-27 22:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_profileuser_tipo_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileuser',
            name='estatura',
            field=models.CharField(default=0, max_length=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profileuser',
            name='peso',
            field=models.CharField(default=0, max_length=7),
            preserve_default=False,
        ),
    ]