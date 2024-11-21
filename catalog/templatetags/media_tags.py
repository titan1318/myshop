from django import template
from django.conf import settings

register = template.Library()

@register.filter
def mymedia(path):
    if path:
        return f'{settings.MEDIA_URL}{path}'
    return '#'
