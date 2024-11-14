from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import (DetailView, ListView, RedirectView,
                                  TemplateView)

from shop.cart.cart import Cart
from shop.models import Category, Product


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


class CategoryProductsListView(ListView):
    model = Product
    template_name = "shop/category_products_list.html"
    context_object_name = "products"
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_name"] = Category.objects.get(pk=self.kwargs["pk"]).name
        return context

    def get_queryset(self):
        category_ids = Category.objects.filter(parent__id=self.kwargs["pk"]).values("id")
        return Product.objects.filter(
            Q(category_id=self.kwargs["pk"]) | Q(category_id__in=category_ids)
        ).prefetch_related("images")


class CartTemplateView(TemplateView):
    template_name = "shop/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context["cart"] = cart
        context["total_price"] = cart.get_total_price()
        return context


class CartAddRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return self.request.META.get("HTTP_REFERER", reverse("index"))

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(pk=request.POST["product_id"])
        cart = Cart(request)
        cart.add(product)

        return redirect(self.get_redirect_url(*args, **kwargs))


class CartChangeAmountRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return self.request.META.get("HTTP_REFERER", reverse("index"))

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(pk=request.POST["product_id"])
        quantity = int(request.POST["quantity"])

        if 0 < quantity <= 100:
            cart = Cart(request)
            cart.add(product, quantity, True)

        return redirect(self.get_redirect_url(*args, **kwargs))


class CartRemoveRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return self.request.META.get("HTTP_REFERER", reverse("index"))

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(pk=request.POST["product_id"])
        cart = Cart(request)
        cart.remove(product)

        return redirect(self.get_redirect_url(*args, **kwargs))
