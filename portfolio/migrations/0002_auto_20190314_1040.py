# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-03-14 02:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userholding',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]