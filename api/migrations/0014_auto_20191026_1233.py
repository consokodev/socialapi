# Generated by Django 2.2.6 on 2019-10-26 12:33

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20191026_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 26, 12, 33, 34, 865185, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userotp',
            name='uid',
            field=models.CharField(max_length=255, primary_key=True, serialize=False, unique=True),
        ),
    ]
