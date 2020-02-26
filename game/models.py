from django.db import models
import datetime
from django.db.models.constraints import UniqueConstraint
from random import randint
from django.apps import apps
import datetime 
from django.utils import timezone

# Create your models here.
'''
The is the place where the structure of database goes
'''
class Game(models.Model):
    
    game_id = models.IntegerField(primary_key=True, default=00000)
    game_mode = models.CharField(max_length=200, default="default")
    player_or_bot = models.CharField(max_length=200, default="default")

    #under turns tab
    max_turns = models.IntegerField(default=0)
    max_seconds_per_turn = models.IntegerField(default=0)

    #under bank accoun tab
    initial_bank_balance = models.IntegerField(default=0)

    #under demand tab
    price_output_equal_player = models.IntegerField(default=0)
    demand_elasticity = models.FloatField(default=0.0)
    price_growth_multiplier = models.FloatField(default=0.0)

    #under R&D tab
    max_value = models.IntegerField(default=0)
    mode = models.IntegerField(default=0)

    #under robots tab
    robot_num = models.IntegerField(default=0)

    #under information tab
    market_report_available = models.BooleanField(default=False)
    report_cost = models.IntegerField(default=0)
    demand_curve_viewable = models.BooleanField(default=False)
    rd_distribution_viewable = models.BooleanField(default=False)

    #game turn_num starting with 0
    turn_num = models.IntegerField(default=0)
    counter_time = models.DateTimeField("Time Submitted", default=timezone.now)

    creator = models.ForeignKey('Company', on_delete=models.DO_NOTHING, related_name='+', default=None, null=True, blank=True)

    #return number of companies in this game
    def company_num(self):
        Game = apps.get_model('game','Game')
        Company = apps.get_model('game','Company')
        game = Game.objects.get(pk=self.game_id)
        return len(Company.objects.filter(game=game))

class Company(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    company_id = models.IntegerField(default=randint(100000000,999999999))
    class Meta:
        constraints  = [
            UniqueConstraint(fields = ['game','company_id'], name='unique_company')
        ]
    machine_purchased = models.IntegerField(default=0)
    to_own = models.IntegerField(default=0)
    machine_operated = models.IntegerField(default=0)
    r_d_purchased = models.IntegerField(default=0)
    bank_balance = models.IntegerField(default=0)
    mp_cost = models.IntegerField(default=0)
    mo_cost = models.IntegerField(default=0)
    r_d_cost = models.IntegerField(default=0)
    revenue = models.IntegerField(default=0)
    unit_produce = models.FloatField(default=0)
    cost_per_turn = models.IntegerField(default=0)

    company_name = models.TextField(default='Untitled')

class Record(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    turn = models.IntegerField(default=1)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    
    class Meta:
        constraints  = [
            UniqueConstraint(fields = ['game','turn','company'], name='unique_record')
        ]

    machine_purchased = models.IntegerField(default=0)
    to_own = models.IntegerField(default=0)
    machine_operated = models.IntegerField(default=0)
    r_d_purchased = models.IntegerField(default=0)
    bank_balance = models.IntegerField(default=0)
    mp_cost = models.IntegerField(default=0)
    mo_cost = models.IntegerField(default=0)
    r_d_cost = models.IntegerField(default=0)
    revenue = models.IntegerField(default=0)
    unit_produce = models.FloatField(default=0)
    cost_per_turn = models.IntegerField(default=0)