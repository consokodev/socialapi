# Generated by Django 2.2.6 on 2019-10-24 01:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20191018_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 24, 1, 56, 35, 276112, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='fb_id',
            field=models.CharField(db_index=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.BooleanField(choices=[('1', 'MALE'), ('2', 'FEMALE'), ('3', 'OTHERS')], max_length=1, null=True),
        ),
    ]
