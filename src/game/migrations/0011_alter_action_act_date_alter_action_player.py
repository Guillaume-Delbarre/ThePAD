# Generated by Django 4.0.1 on 2022-02-08 17:49

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_player_remove_action_user_action_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='act_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 8, 17, 49, 40, 123546, tzinfo=utc), verbose_name='action date'),
        ),
        migrations.AlterField(
            model_name='action',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.player'),
        ),
    ]