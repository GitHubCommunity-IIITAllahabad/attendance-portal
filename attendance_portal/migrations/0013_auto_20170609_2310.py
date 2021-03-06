# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-09 23:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_portal', '0012_auto_20170609_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='lecture',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='attendance_portal.Lecture'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attendancetoken',
            name='lecture',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='attendance_portal.Lecture'),
            preserve_default=False,
        ),
    ]
