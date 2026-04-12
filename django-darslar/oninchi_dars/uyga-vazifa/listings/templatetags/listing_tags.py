from django import template

register = template.Library()

@register.filter(name='human_price')
def human_price(value):
    """
    Formats a number with spaces as thousand separators.
    e.g., 1000000 -> 1 000 000
    """
    try:
        price = int(value)
        return f"{price:,}".replace(',', ' ')
    except (ValueError, TypeError):
        return value
