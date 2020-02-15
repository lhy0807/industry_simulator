# Generated by Django 3.0.2 on 2020-02-06 03:31

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('game_id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('game_mode', models.CharField(default='default', max_length=200)),
                ('player_or_bot', models.CharField(default='default', max_length=200)),
                ('max_turns', models.IntegerField(default=0)),
                ('max_seconds_per_turn', models.IntegerField(default=0)),
                ('initial_bank_balance', models.IntegerField(default=0)),
                ('price_output_equal_player', models.IntegerField(default=0)),
                ('demand_elasticity', models.FloatField(default=0.0)),
                ('price_growth_multiplier', models.FloatField(default=0.0)),
                ('max_value', models.IntegerField(default=0)),
                ('mode', models.IntegerField(default=0)),
                ('robot_num', models.IntegerField(default=0)),
                ('market_report_available', models.BooleanField(default=False)),
                ('report_cost', models.IntegerField(default=0)),
                ('demand_curve_viewable', models.BooleanField(default=False)),
                ('rd_distribution_viewable', models.BooleanField(default=False)),
                ('turn_num', models.IntegerField(default=1)),
                ('counter_time', models.DateTimeField(default=datetime.datetime(2020, 2, 5, 22, 31, 30, 899887), verbose_name='Time Submitted')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.IntegerField(default=444224409)),
                ('machine_purchased', models.IntegerField(default=0)),
                ('machine_operated', models.IntegerField(default=0)),
                ('r_d_purchased', models.IntegerField(default=0)),
                ('bank_balance', models.IntegerField(default=0)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Game')),
            ],
        ),
        migrations.AddConstraint(
            model_name='company',
            constraint=models.UniqueConstraint(fields=('game', 'company_id'), name='unique_company'),
        ),
    ]
