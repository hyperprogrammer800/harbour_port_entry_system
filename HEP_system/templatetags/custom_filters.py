from django import template

register = template.Library()

@register.filter
def display_related(value, field):
    """Display a related object's string representation, or a default if None."""
    
    return str(getattr(value,field.name))

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, '')

@register.filter
def multiply_filter(a,b):
    return ((b-1)*10) + a

@register.filter
def add(a,b):
    return a+b

@register.filter
def sub(a,b):
    return a-b