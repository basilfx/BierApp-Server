from django.http import QueryDict
from django import template

import math

register = template.Library()

@register.simple_tag
def estimate_count(product_group, product):
    try:
        return int(math.floor(product_group.total_value / product.value))
    except ZeroDivisionError:
        return 0
