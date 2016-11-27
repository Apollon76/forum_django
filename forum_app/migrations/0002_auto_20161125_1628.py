# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('user_id', models.IntegerField()),
                ('nickname', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('registration_date', models.DateTimeField()),
            ],
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]
