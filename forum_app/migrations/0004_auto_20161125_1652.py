# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_app', '0003_remove_user_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='registration_date',
            field=models.DateTimeField(null=True),
        ),
    ]
