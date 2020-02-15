from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from random import randint
from django.urls import reverse
from .models import *
import time
import logging

# Create your views here.
def index(request, game_id, company_id):
    game = get_object_or_404(Game, pk=game_id)
    company = get_object_or_404(Company, game=game, company_id=company_id)
    record = Record.objects.filter(game=game,company=company)
    request.session['game']=game_id
    request.session['company']=company_id
    return render(request, 'game/index.html', {'game':game,'company':company,'record':record})

def save_to_record(game, company, turn=1):
    record = Record(game=game, turn=turn, company=company)
    record.machine_purchased = company.machine_purchased
    record.to_own = company.to_own
    record.machine_operated = company.machine_operated
    record.r_d_purchased = company.r_d_purchased
    record.bank_balance = company.bank_balance
    record.mp_cost = company.mp_cost
    record.mo_cost = company.mo_cost
    record.r_d_cost = company.r_d_cost
    record.revenue = company.revenue
    record.unit_produce = company.unit_produce
    record.cost_per_turn = company.cost_per_turn
    record.save()

def create(request):
    '''
        Initialize Game model
    '''
    try:
        #from create_group
        game_id = request.POST['game_id']
        company_id = request.POST['company_id']
        game = Game.objects.get(game_id=game_id,player_or_bot='player')
        company = Company.objects.get(game=game, company_id=company_id)
    except(Exception):
        #from create_bot
        #generate a 10-digit random game id
        game_id = randint(10000, 99999)
        #even though very unlikely, still test for existence of this random ID
        try:
            Game.objects.get(pk=game_id)
            #regenerate another ID
            game_id = randint(1000000000, 9999999999)
        except Game.DoesNotExist:
            next
        game = Game(pk=game_id, player_or_bot='bot')
        game.save()
        '''
        Initialize Company Model
        '''
        #hard_coded id. need to be changed
        company_id = 100000000
        company = Company(game=game,company_id=company_id)
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
            game.save()

        company.bank_balance = game.initial_bank_balance
        company.mp_cost = 1000
        company.mo_cost = 5000
        company.save()

        if len(Record.objects.filter(game=game, turn=1, company=company)) == 0:
            save_to_record(game=game, company=company)

    except(KeyError):
            return HttpResponse("POST Error")
    

    return HttpResponseRedirect(reverse('game:index', args=(game_id,company_id)))

def update(request, game_id, company_id):
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
        if game_mode != 'simple_production':
            r_d = request.POST['r_d']
        
        #update company
        company.machine_purchased = mp
        company.to_own += mp
        company.machine_operated = mo

        #game_mode == 'simple_production'
        company.unit_produce = mo
        company.cost_per_turn = mp*company.mp_cost + mo*company.mo_cost
        #TODO:game_mode == others

        company.bank_balance -= company.cost_per_turn
        
        
        '''
        save data
        '''
        game.save()
        company.save()
        save_to_record(game, company, turn=game.turn_num+1)

    except(KeyError):
        return HttpResponse("POST Error")
    
    return HttpResponseRedirect(reverse('game:wait', args=(game_id,company_id,game.turn_num)))


def continue_game(request):
    game_id = request.session['game']
    company_id = request.session['company']
    return HttpResponseRedirect(reverse('game:index', args=(game_id,company_id)))

def wait(request, game_id, company_id, turn_num):
    game = Game.objects.get(game_id=game_id)
    company_list = Company.objects.filter(game=game)

    while True:
        # to reduce the pressure of server
        # half sec delay
        time.sleep(0.5)
        ready = True
        for company in company_list:
            tmp = Record.objects.filter(game=game, company=company, turn=turn_num+1)
            if len(tmp) == 0:
                ready = False
                continue
        if ready:
            break
    '''
    Operations when everyone is ready
    '''
    #calculate the total quantity produced/supplied
    record_list = Record.objects.filter(game=game, turn=turn_num+1)
    Q = 0
    for record in record_list:
        Q += record.unit_produce

    '''
    DEFINE REVERSE DEMAND CURVE HERE
    '''
    if Q == 0:
        Q = 0.01
    P = 20000 / Q

    #assign revenue for the company
    for record in record_list:
        if record.company.company_id == company_id:
            record.revenue = record.unit_produce * P
            record.company.revenue = record.unit_produce * P

            record.bank_balance += record.revenue
            record.company.bank_balance += record.revenue

            record.company.save()
            record.save()

    #increase game turn by 1
    game.turn_num += 1
    game.save()

    return HttpResponseRedirect(reverse('game:index', args=(game_id,company_id)))