# Generated by Django 4.0.1 on 2022-11-19 16:18

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_alter_action_act_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date')),
                ('fini', models.BooleanField(default=False)),
                ('nom', models.CharField(max_length=50)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='game.player')),
            ],
        ),
        migrations.CreateModel(
            name='MiseJoueur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mise_score', models.PositiveIntegerField()),
                ('resultat', models.BooleanField(default=False)),
                ('mise_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date')),
                ('mise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.mise')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.player')),
            ],
        ),
    ]