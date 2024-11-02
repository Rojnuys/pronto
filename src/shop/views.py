from django.shortcuts import render
from django.views.generic import DetailView, ListView

from shop.models import Product


# Create your views here.
class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self):
        return Product.objects.all().prefetch_related("images")


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.all().prefetch_related("images").prefetch_related("related_products")
