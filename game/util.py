# Helper Function
from .models import *


def save_to_record(game, company, turn=0):
    exist = len(Record.objects.filter(
        game=game, turn=turn, company=company)) != 0
    if not exist:
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


def r_d_draw_to_cost(draw):
    # TODO: use a naivce calculation for cost
    return draw**2*1000
