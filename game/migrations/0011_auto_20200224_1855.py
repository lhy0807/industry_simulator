# Generated by Django 3.0.2 on 2020-02-24 23:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_auto_20200224_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='company_id',
            field=models.IntegerField(default=832375934),
        ),
        migrations.AlterField(
            model_name='game',
            name='counter_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Time Submitted'),
        ),
    ]