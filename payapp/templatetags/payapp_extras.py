from django import template

register = template.Library()


def currency_to_sign(value):
    if value == 'USD':
        return '$'
    elif value == 'EUR':
        return '€'
    else:
        return '£'


register.filter(currency_to_sign)
