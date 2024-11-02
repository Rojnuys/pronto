import random
import string

from django import template

register = template.Library()


@register.simple_tag
def get_random_text():
    return "".join(random.choices(string.ascii_lowercase, k=8))
