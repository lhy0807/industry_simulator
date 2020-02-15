from django import template
from django.apps import apps

register = template.Library()
@register.filter(name='get_machine_purchased')
def get_machine_purchased(record, turn):
    return record.get(turn=turn).machine_purchased

@register.filter(name='get_to_own')
def get_to_own(record, turn):
    return record.get(turn=turn).to_own

@register.filter(name='get_machine_operated')
def get_machine_operated(record, turn):
    return record.get(turn=turn).machine_operated

@register.filter(name='get_r_d_purchased')
def get_r_d_purchased(record, turn):
    return record.get(turn=turn).r_d_purchased

@register.filter(name='get_mp_cost')
def get_mp_cost(record, turn):
    return record.get(turn=turn).mp_cost * record.get(turn=turn).machine_purchased

@register.filter(name='get_mo_cost')
def get_mo_cost(record, turn):
    return record.get(turn=turn).mo_cost * record.get(turn=turn).machine_operated

@register.filter(name='get_r_d_cost')
def get_r_d_cost(record, turn):
    return record.get(turn=turn).r_d_cost

@register.filter(name='get_revenue')
def get_revenue(record, turn):
    return record.get(turn=turn).revenue

@register.filter(name='get_unit_produce')
def get_unit_produce(record, turn):
    return record.get(turn=turn).unit_produce

@register.filter(name='get_cost_per_turn')
def get_cost_per_turn(record, turn):
    return record.get(turn=turn).cost_per_turn

@register.filter(name='get_bank_balance')
def get_bank_balance(record, turn):
    return record.get(turn=turn).bank_balance

@register.filter(name='get_initial')
def get_get_initial(record, turn):
    if turn > 1:
        return record.get(turn=turn-1).bank_balance
    return 0

@register.filter(name='get_before_revenue')
def get_before_revenue(record, turn):
    return record.get(turn=turn).bank_balance - record.get(turn=turn).revenue