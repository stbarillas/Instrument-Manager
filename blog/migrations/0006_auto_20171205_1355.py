# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-05 21:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20171205_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklist',
            name='ownership_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 5, 21, 55, 5, 846295, tzinfo=utc)),
        ),
    ]
