# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_app', '0009_thread'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='posts',
            field=models.ManyToManyField(to='forum_app.Post'),
        ),
    ]
