# Generated by Django 4.0.1 on 2022-06-24 16:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_alter_action_act_date_alter_player_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='act_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 24, 16, 23, 44, 19369, tzinfo=utc), verbose_name='action date'),
        ),
    ]
