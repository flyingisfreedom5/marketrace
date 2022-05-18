from atexit import register
from django import template

register = template.Library()

@register.filter
def percChange(val1, arg):
    return round(((int(val1) / int(arg)) -1), 2)

# register.filter('divide', divide)