from django import template

register = template.Library()

@register.filter
def lookup(cart, product_id):
    """
    Возвращает количество товара в корзине по ID
    """
    return cart.cart.get(str(product_id), {}).get('quantity', 0)