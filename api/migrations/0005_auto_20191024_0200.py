# Generated by Django 2.2.6 on 2019-10-24 02:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20191024_0156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 24, 2, 0, 49, 280458, tzinfo=utc)),
        ),
    ]
