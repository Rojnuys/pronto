from django import template

from shop.models import Category

register = template.Library()


@register.simple_tag
def get_catalog_data():
    return Category.objects.exclude(parent__isnull=False).prefetch_related("children")
