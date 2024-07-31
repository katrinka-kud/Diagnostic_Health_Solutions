from django import template

register = template.Library()


# Создание тега
@register.filter()
def mymedia(val):
    if val:
        return f'/media/{val}'
    return '#'
