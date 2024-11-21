import random
import string
from decimal import Decimal

from django.core.files.base import ContentFile
from faker import Faker

from common.utils.helpers import fetch_pic
from shop.models import (Category, Comment, Product, ProductImage, Rating,
                         RelatedProduct, Status)


def generate_fake_categories(count: int = 10):
    fake = Faker()
    for i in range(count):
        category = Category(name=fake.word())
        category_ids = Category.objects.all().values_list("pk", flat=True)
        if category_ids.count() > 0:
            category.parent_id = None if random.randint(1, 10) == 1 else random.choice(category_ids)
        category.save()


def generate_fake_comments(count: int = 10):
    fake = Faker()
    for i in range(count):
        comment = Comment(product=Product.objects.order_by("?").first(), content=fake.text(max_nb_chars=50))
        if random.randint(1, 3) == 1:
            comment.advantages = fake.text(max_nb_chars=30)
        if random.randint(1, 3) == 1:
            comment.disadvantages = fake.text(max_nb_chars=30)
        comment.rating = Rating(random.randint(1, 5))
        comment.is_allowed = True
        comment.save()


def generate_fake_products(count: int = 10):
    fake = Faker()
    for i in range(count):
        product = Product(
            name=fake.sentence(nb_words=5),
            price=f"{random.randint(0, 99999999)}.{random.randint(1, 99)}",
            description=fake.text(max_nb_chars=500),
        )
        product.category = Category.objects.order_by("?").first()
        attributes = {}
        for j in range(random.randint(1, 15)):
            attributes[fake.sentence(nb_words=random.randint(1, 3))] = fake.sentence(nb_words=random.randint(1, 10))
        product.attributes = attributes
        if random.randint(1, 5) == 1:
            product.sale_price = Decimal(product.price) - int(Decimal(product.price) / random.randint(2, 10))
            product.is_sale = True
        if random.randint(1, 5) == 1:
            product.status = Status.INACTIVE
        if random.randint(1, 5) == 1:
            product.status = Status.OUT_OF_STOCK

        product.save()

        for j in range(random.randint(0, 5)):
            try:
                RelatedProduct.objects.create(product=product, related_product=Product.objects.order_by("?").first())
            except Exception:
                ...

        for j in range(random.randint(0, 3)):
            try:
                ProductImage.objects.create(
                    product=product,
                    image=ContentFile(
                        fetch_pic(), name="".join(random.choices(string.ascii_letters + string.digits, k=10))
                    ),
                    order_number=j + 1,
                )
            except Exception:
                ...
