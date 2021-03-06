# Generated by Django 4.0.1 on 2022-03-30 19:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_player_id_alter_action_act_date_alter_player_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='act_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 30, 19, 12, 11, 158444, tzinfo=utc), verbose_name='action date'),
        ),
        migrations.AlterField(
            model_name='player',
            name='description',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
