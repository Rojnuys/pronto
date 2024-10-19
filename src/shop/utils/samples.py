from shop.models import Category, Product, RelatedProduct


def sample_product(name, **params) -> Product:
    default = {
        "category": Category.objects.get_or_create(name="Test category")[0],
        "description": "Test description",
        "price": 10,
    }
    default.update(params)
    return Product.objects.create(name=name, **default)


def sample_related_product(**params) -> RelatedProduct:
    default = {
        "product": sample_product(name="Test product #1"),
        "related_product": sample_product(name="Test product #2"),
    }
    default.update(params)
    return RelatedProduct.objects.create(**default)
