from django import template

register = template.Library()


# Создание тега
@register.filter()
def media_filter(val):
    if val:
        return f'/media/{val}'
    return '#'
