# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-02-06 05:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20171205_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklist',
            name='ownership_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 6, 5, 25, 24, 811029, tzinfo=utc)),
        ),
    ]
