from django import template

register = template.Library()

@register.filter
def invert(value):
    """Invert a stat i.e. resists"""
    return (1 - value) * 100