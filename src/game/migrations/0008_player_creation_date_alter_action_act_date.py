# Generated by Django 4.0.1 on 2022-06-29 16:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_alter_action_act_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 16, 1, 28, 153401, tzinfo=utc), verbose_name='creation date'),
        ),
        migrations.AlterField(
            model_name='action',
            name='act_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 16, 1, 28, 153401, tzinfo=utc), verbose_name='action date'),
        ),
    ]