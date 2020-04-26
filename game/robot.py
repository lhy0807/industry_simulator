from .util import *
import math
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.middleware import csrf
from .models import *
import requests


class Robot:
    def __init__(self, id, name, game_id):
        self.id = id
        self.name = name
        self.game_id = game_id
        self.game = get_object_or_404(Game, pk=self.game_id)

        self.company = Company(
            game=self.game, company_id=self.id, company_name=self.name)

        self.company.bank_balance = self.game.initial_bank_balance
        self.company.mp_cost = 1000
        self.company.mo_cost = 5000

        self.game.save()
        self.company.save()

        save_to_record(game=self.game, company=self.company)

    def update(self):
        # Updata game and company status
        self.game = get_object_or_404(Game, pk=self.game_id)
        self.company = Company.objects.get(
            game=self.game, company_id=self.id, company_name=self.name)


class DoNothingBot(Robot):
    # This is a dummy bot
    def make_decision(self, url):
        # update status
        super().update()

        # DO NOTHING EACH TURN
        mp = 0
        mo = 0
        if self.game.game_mode != 'simple_production':
            r_d = 0

        self.company.machine_purchased = mp
        self.company.to_own += mp
        self.company.machine_operated = mo
        self.company.r_d_purchased = 0
        self.company.r_d_cost = 0
        self.company.unit_produce = 0
        self.company.cost_per_turn = 0

        self.company.save()
        save_to_record(game=self.game, company=self.company,
                       turn=self.game.turn_num+1)


class BuyerBot(Robot):
    '''
    This is Bot is used to test game data calculation
    ONLY BUY MACHINE AS MANY AS POSSIBLE
    '''

    def make_decision(self, url):
        # update status
        super().update()

        mp = 0
        mo = 0
        if self.game.game_mode != 'simple_production':
            r_d = 0

        # Find maximum purchase amount
        mp = math.floor(self.company.bank_balance / self.company.mp_cost)

        self.company.machine_purchased = mp
        self.company.to_own += mp
        self.company.machine_operated = mo
        self.company.r_d_purchased = 0
        self.company.r_d_cost = 0
        self.company.unit_produce = 0
        self.company.cost_per_turn = mp * self.company.mp_cost

        self.company.save()
        save_to_record(game=self.game, company=self.company,
                       turn=self.game.turn_num+1)


class SmarterBot(Robot):
    '''
    This bot is smarter
    First maximize machine operated
    Then maximize machine purchased (Half)
    '''

    def make_decision(self, request):
        # update status
        super().update()

        mp = 0
        mo = 0
        if self.game.game_mode != 'simple_production':
            r_d = 0

        # Find Maximum Operated amount
        mo = min(self.company.to_own, math.floor(
            self.company.bank_balance / self.company.mo_cost))

        # remaining bank balance after operating cost
        remaining = self.company.bank_balance - mo * self.company.mo_cost

        mp = math.floor(remaining / self.company.mp_cost) / 2

        mo = int(mo)
        mp = int(mp)

        self.company.machine_purchased = mp
        self.company.to_own += mp
        self.company.machine_operated = mo
        self.company.r_d_purchased = 0
        self.company.r_d_cost = 0

        if self.game.game_mode == 'simple_production' or self.game.game_mode == 'cost_reduce':
            self.company.unit_produce = mo
        elif self.game.game_mode == 'output_expand':
            self.company.unit_produce = mo * \
                (1+0.04)**self.company.r_d_purchased

        self.company.cost_per_turn = mp * self.company.mp_cost + mo * self.company.mo_cost

        self.company.save()
        save_to_record(game=self.game, company=self.company,
                       turn=self.game.turn_num+1)
