from celery import shared_task

from shop.utils.generate_fake_data import (generate_fake_categories,
                                           generate_fake_comments,
                                           generate_fake_products)


@shared_task
def generate_fake_categories_task():
    generate_fake_categories()


@shared_task
def generate_fake_comments_task():
    generate_fake_comments()


@shared_task
def generate_fake_products_task():
    generate_fake_products()
