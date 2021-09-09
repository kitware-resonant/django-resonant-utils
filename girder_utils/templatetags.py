from django import template

register = template.Library()


@register.filter()
def getitem(value, arg):
    """
    Retrieve value[arg] from a template, where arg can be a variable.
    """
    return value.get(arg, None)
