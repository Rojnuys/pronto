from celery import shared_task

from shop.utils.generate_fake_data import (generate_fake_categories,
                                           generate_fake_comments,
                                           generate_fake_products, generate_fake_slider_items)


@shared_task
def generate_fake_categories_task(count: int = 10):
    generate_fake_categories(count)


@shared_task
def generate_fake_comments_task(count: int = 10):
    generate_fake_comments(count)


@shared_task
def generate_fake_products_task(count: int = 10):
    generate_fake_products(count)


@shared_task
def generate_fake_slider_items_task(count: int = 5):
    generate_fake_slider_items(count)
