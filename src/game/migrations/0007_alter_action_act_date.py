# Generated by Django 4.0.1 on 2022-06-29 15:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_alter_action_act_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='act_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 15, 44, 44, 512383, tzinfo=utc), verbose_name='action date'),
        ),
    ]
