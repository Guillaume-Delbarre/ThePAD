# Generated by Django 4.0.1 on 2022-06-29 16:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_player_creation_date_alter_action_act_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='creation_date',
        ),
        migrations.AlterField(
            model_name='action',
            name='act_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 16, 5, 19, 246435, tzinfo=utc), verbose_name='action date'),
        ),
    ]
