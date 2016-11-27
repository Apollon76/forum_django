# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum_app', '0007_auto_20161125_1805'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('data', models.CharField(max_length=100000)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, to='forum_app.User')),
            ],
        ),
    ]
