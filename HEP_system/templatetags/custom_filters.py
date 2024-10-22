from django import template

register = template.Library()

@register.filter
def display_related(value, field):
    """Display a related object's string representation, or a default if None."""
    print(value.id,"OBJECT ID")
    return str(getattr(value,field.name))