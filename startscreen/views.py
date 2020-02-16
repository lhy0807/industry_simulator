from django.shortcuts import render
from random import randint
from django.http import HttpResponse
from django.apps import apps


def index(request):
    Game = apps.get_model('game','Game')
    #generate a 10-digit random game id
    game_id = randint(10000, 99999)
    company_id = randint(100000000,999999999)
    #even though very unlikely, still test for existence of this random ID
    try:
        Game.objects.get(pk=game_id)
        #regenerate another ID
        game_id = randint(10000, 99999)
    except Game.DoesNotExist:
        next
    return render(request, 'startscreen/index.html',{'game_id':game_id,'company_id':company_id})

def create_robot(request):
    has_previous_game = True
    Game = apps.get_model('game','Game')
    Company = apps.get_model('game','Company')
    try:
        game_id = request.session['game']
        company_id = request.session['company']
        game = Game.objects.get(game_id=game_id,player_or_bot='bot')
        company = Company.objects.get(game=game,company_id=company_id)
    except(Exception):
        has_previous_game = False
        
    return render(request, 'startscreen/create_robot.html', {'has_previous_game':has_previous_game})

def create_group(request, game_id, company_id):
    Game = apps.get_model('game','Game')
    Company = apps.get_model('game','Company')
    is_creator = False
    try:
        game = Game.objects.get(pk=game_id, player_or_bot='player')
    except Exception:
        game = Game(pk=game_id, player_or_bot='player')
        game.save()

    try:
        company = Company.objects.get(game=game,company_id=company_id)
    except Exception:
        company = Company(game=game,company_id=company_id)
        company.save()

        #First one creates a game is creator
        if game.creator is None:
            game.creator = company
            game.save()
            is_creator = True

    if game.creator == company:
        is_creator = True
    
    company_list = Company.objects.filter(game=game)

    return render(request, 'startscreen/create_group.html', {'game':game, 'company':company,'company_list':company_list,'is_creator':is_creator})

def join_group(request, game_id, company_id):
    Game = apps.get_model('game','Game')
    Company = apps.get_model('game','Company')
    game = Game.objects.get(pk=game_id, player_or_bot='player')
    try:
        company = Company.objects.get(game=game,company_id=company_id)
    except Exception:
        company = Company(game=game,company_id=company_id)
        company.save()
    company_list = Company.objects.filter(game=game)

    '''
    Detect is a game is joinable
    Using a naive method which is detect whether is time per turn
    is still 0
    TODO: Can be subsituted by a more robust detection in the future
    '''
    joinable = False
    if game.max_seconds_per_turn != 0:
        joinable = True

    return render(request, 'startscreen/join_group.html', {'game':game, 'company':company,'company_list':company_list,'joinable':joinable})