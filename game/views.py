from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from random import randint
from django.urls import reverse
from .models import *
import datetime
import logging
import time
from django.utils import timezone
from .util import *
from .robot import *


class AgentList:
    def __init__(self):
        self.list = []

    def add(self, agent):
        self.list.append(agent)

    def make_decision(self):
        for i in range(len(self.list)):
            self.list[i].make_decision()


# Instantiate an agent list
agents = AgentList()


def index(request, game_id, company_id):
    # Index Page here
    game = get_object_or_404(Game, pk=game_id)
    company = get_object_or_404(Company, game=game, company_id=company_id)
    record = Record.objects.filter(game=game, company=company)
    request.session['game'] = game_id
    request.session['company'] = company_id
    error = ''
    try:
        error = request.session['error']
        request.session['error'] = ''
    except(Exception):
        next
    return render(request, 'game/index.html', {'game': game, 'company': company, 'record': record, 'error': error})


def create(request):
    # Create a game
    # Initialize Game model
    try:
        '''
        For group game
        from create_group
        '''
        game_id = request.POST['game_id']
        company_id = request.POST['company_id']
        game = Game.objects.get(game_id=game_id, player_or_bot='player')
        company = Company.objects.get(game=game, company_id=company_id)
    except(Exception):
        '''
        from create_bot
        generate a 10-digit random game id
        '''
        game_id = randint(10000, 99999)
        # even though very unlikely, still test for existence of this random ID
        try:
            Game.objects.get(pk=game_id)
            # regenerate another ID
            game_id = randint(10000, 99999)
        except Game.DoesNotExist:
            next
        game = Game(pk=game_id, player_or_bot='bot')
        game.save()

        # Initialize Player's Company Model for robot game
        company_id = 100000000
        company = Company(game=game, company_id=company_id)
        company.save()

    try:
        if game.player_or_bot == 'bot' or game.creator == company:
            game.game_mode = request.POST['game_mode']
            game.max_seconds_per_turn = request.POST['max_seconds_per_turn']
            game.initial_bank_balance = request.POST['initial_bank_balance']
            game.price_output_equal_player = request.POST['price_output_equal_player']
            game.demand_elasticity = request.POST['demand_elasticity']
            game.price_growth_multiplier = request.POST['price_growth_multiplier']
            game.max_value = request.POST['max_value']
            game.mode = request.POST['mode']
            game.robot_num = request.POST['robot_num']

            if request.POST['market_report_available'] == 'on':
                game.market_report_available = True
            else:
                game.market_report_available = False

            if request.POST['demand_curve_viewable'] == 'on':
                game.demand_curve_viewable = True
            else:
                game.demand_curve_viewable = False

            if request.POST['rd_distribution_viewable'] == 'on':
                game.rd_distribution_viewable = True
            else:
                game.rd_distribution_viewable = False
            game.counter_time = timezone.now()
            game.save()

        company.bank_balance = game.initial_bank_balance
        company.mp_cost = 1000
        company.mo_cost = 5000
        company.save()

        # prevent saving exisiting record
        if len(Record.objects.filter(game=game, turn=0, company=company)) == 0:
            save_to_record(game=game, company=company)

        if game.player_or_bot == 'bot':
            '''
            Create robot agents instances HERE:
            '''
            global agents
            agents.add(DoNothingBot(
                id=1000000001, name='DoNothingBot', Game=Game, game_id=game_id, Company=Company))
            agents.add(BuyerBot(
                id=1000000002, name='BuyerBot', Game=Game, game_id=game_id, Company=Company))
            agents.add(SmarterBot(
                id=1000000003, name='SmarterBot', Game=Game, game_id=game_id, Company=Company))
            agents.add(SmarterBot(
                id=1000000004, name='SmarterBot', Game=Game, game_id=game_id, Company=Company))
            agents.add(SmarterBot(
                id=1000000005, name='SmarterBot', Game=Game, game_id=game_id, Company=Company))

    except(KeyError):
        return HttpResponse("POST Error")

    return HttpResponseRedirect(reverse('game:index', args=(game_id, company_id)))

# Update a game


def update(request, game_id, company_id):
    '''
    Idea:
    Assign values to temporary variables
    Apply Detection Mechanism
    Change values of company according to temp variables
    '''
    try:

        game_id = game_id
        company_id = company_id
        game = Game.objects.get(game_id=game_id)
        company = Company.objects.get(game=game, company_id=company_id)

        '''
        game_mode
        - 'simple_production'
        - 'cost_reduce'
        - 'output_expand'
        '''
        game_mode = game.game_mode

        mp = int(request.POST['mp'])
        mo = int(request.POST['mo'])
        tmp_mo_cost = company.mo_cost
        tmp_mp_cost = company.mp_cost
        tmp_r_d_cost = company.r_d_cost
        tmp_r_d_purchased = company.r_d_purchased

        # calculate R&D
        if game_mode != 'simple_production':
            r_d = int(request.POST['r_d'])
            tmp_r_d_purchased = company.r_d_purchased + r_d
            tmp_r_d_cost = r_d_draw_to_cost(r_d)

        # reduce cost if in cost_reduce mode
        if game_mode == 'cost_reduce':
            # TODO: improve cost reduction method
            tmp_mo_cost = tmp_mo_cost * (1-0.04)**tmp_r_d_purchased

        #game_mode == 'simple_production' or 'cost_reduce'
        if game_mode == 'simple_production' or game_mode == 'cost_reduce':
            tmp_unit_produce = mo
        #game_mode == 'output_expand'
        # increase produced unit if in output_expand mode
        elif game_mode == 'output_expand':
            tmp_unit_produce = mo * (1+0.04)**tmp_r_d_purchased

        tmp_cost_per_turn = mp*tmp_mp_cost + mo*tmp_mo_cost + tmp_r_d_cost

        # apply detection mechanism
        # 1. If machine operated larger than to_own
        if mo > company.to_own + mp:
            error = 'Machine Operated larger than Machine Owned'
            request.session['error'] = error
            return HttpResponseRedirect(reverse('game:index', args=(game_id, company_id)))
        # 2. If cost_per_turn larger than bank balance
        if tmp_cost_per_turn > company.bank_balance:
            error = 'Cost Per Turn Larger than Bank Balance'
            request.session['error'] = error
            return HttpResponseRedirect(reverse('game:index', args=(game_id, company_id)))

        # after verification mechanism
        # update company using tmp variables
        company.machine_purchased = mp
        company.to_own += mp
        company.machine_operated = mo
        company.r_d_purchased = tmp_r_d_purchased
        company.r_d_cost = tmp_r_d_cost
        company.mo_cost = tmp_mo_cost
        company.unit_produce = tmp_unit_produce
        company.cost_per_turn = tmp_cost_per_turn
        # deduct bank balance
        company.bank_balance -= company.cost_per_turn
        '''
        save data
        '''
        game.save()
        company.save()
        save_to_record(game, company, turn=game.turn_num+1)

        '''
        Robot Agents take actions after human player
        '''
        agents.make_decision()
    except(KeyError):
        return HttpResponse("POST Error")

    return HttpResponseRedirect(reverse('game:wait', args=(game_id, company_id, game.turn_num)))


def continue_game(request):
    game_id = request.session['game']
    company_id = request.session['company']
    return HttpResponseRedirect(reverse('game:index', args=(game_id, company_id)))


def wait(request, game_id, company_id, turn_num):
    game = Game.objects.get(game_id=game_id)
    company_list = Company.objects.filter(game=game)

    while True:
        # to reduce the pressure of server
        # half sec delay
        time.sleep(0.5)
        ready = True
        for company in company_list:
            tmp = Record.objects.filter(
                game=game, company=company, turn=turn_num+1)
            if len(tmp) == 0:
                ready = False
                continue
        if ready:
            break
    '''
    Operations when everyone is ready
    '''
    # calculate the total quantity produced/supplied
    record_list = Record.objects.filter(game=game, turn=turn_num+1)
    Q = 0
    for record in record_list:
        Q += record.unit_produce

    '''
    DEFINE REVERSE DEMAND CURVE HERE
    '''
    K = game.price_output_equal_player / \
        (game.company_num()**(-1/game.demand_elasticity))
    if Q == 0:
        Q = 1
    P = K * Q**(-1/game.demand_elasticity) * \
        game.price_growth_multiplier**turn_num

    # assign revenue for the company
    for record in record_list:
        if record.company.company_id == company_id:
            record.revenue = record.unit_produce * P
            record.company.revenue = record.unit_produce * P

            record.bank_balance += record.revenue
            record.company.bank_balance += record.revenue

            record.company.save()
            record.save()

    # update game turn timer
    game.counter_time = timezone.now()

    # increase game turn by 1
    game.turn_num += 1
    game.save()

    return HttpResponseRedirect(reverse('game:index', args=(game_id, company_id)))
