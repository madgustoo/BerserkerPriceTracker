# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-14 06:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volumes', '0002_auto_20170114_0354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='publication_date',
            field=models.DateField(null=True, verbose_name='date published'),
        ),
    ]