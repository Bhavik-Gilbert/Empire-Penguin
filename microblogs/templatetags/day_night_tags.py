import datetime

from django import template

register = template.Library()

@register.filter
def is_day(time):
    return datetime.time(6, 0, 0) <= datetime.datetime.now().time() and datetime.datetime.now().time() <= datetime.time(18, 0, 0)