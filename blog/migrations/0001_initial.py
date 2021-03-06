# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-27 00:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=50)),
                ('instrument_pk', models.IntegerField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instrument_type', models.CharField(choices=[('LC', 'LC'), ('LCMS', 'LCMS'), ('GC', 'GC'), ('GCMS', 'GCMS')], default='LC', max_length=4)),
                ('instrument_status', models.CharField(choices=[('Available', 'Available'), ('In Use', 'In Use'), ('Out of Order', 'Out of Order')], default='Available', max_length=50)),
                ('ip_address', models.GenericIPAddressField(protocol='IPv4')),
                ('instrument_name', models.CharField(max_length=50)),
                ('instrument_image', models.ImageField(upload_to='images')),
                ('instrument_connection', models.BooleanField(default=True)),
                ('instrument_current_owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(blank=True, help_text='Optional', max_length=254)),
                ('receive_email_notifications', models.BooleanField(default=False)),
                ('mobile_number', models.CharField(blank=True, help_text='Optional', max_length=15)),
                ('mobile_carrier', models.CharField(blank=True, choices=[(None, ''), ('@txt.att.net', 'AT&T'), ('@messaging.sprintpcs.com', 'Sprint'), ('@tmomail.net', 'T-Mobile'), ('@vtext.com', 'Verizon')], help_text='Optional', max_length=25)),
                ('receive_sms_notifications', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='instrument',
            unique_together=set([('instrument_type', 'ip_address')]),
        ),
    ]
