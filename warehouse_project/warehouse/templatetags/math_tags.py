# warehouse/templatetags/math_tags.py
from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """
    Умножает value на arg.
    Пример в шаблоне: {{ item.quantity|multiply:item.product.price }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''