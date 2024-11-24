from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (DetailView, ListView, RedirectView,
                                  TemplateView, CreateView)

from shop.cart.cart import Cart
from shop.forms import OrderForm, CommentForm
from shop.models import Category, Product, Order, OrderProduct, Comment
from shop.tasks import (generate_fake_categories_task,
                        generate_fake_comments_task,
                        generate_fake_products_task)


# Create your views here.
class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self):
        return Product.objects.all().prefetch_related("images")


class ProductSearchListView(ListView):
    model = Product
    context_object_name = "products"
    template_name = "shop/product_list.html"
    paginate_by = 20

    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get("search", "").strip()).prefetch_related("images")


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.all().prefetch_related("images").prefetch_related("related_products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["average_rating"] = self.get_object().comments.filter( is_allowed=True).aggregate(average_rating=Avg("rating"))["average_rating"]
        if context["average_rating"]:
            context["average_rating"] = round(context["average_rating"], 1)
        else:
            context["average_rating"] = 0
        context["comment_count"] = self.get_object().comments.filter( is_allowed=True).count()
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = self.get_object()
            comment.save()
            return HttpResponseRedirect(reverse("shop:product_detail", kwargs={"pk": self.get_object().pk}))
        return self.render_to_response(self.get_context_data(form=form))


class CommentListView(ListView):
    model = Comment
    context_object_name = "comments"
    paginate_by = 10

    def get_queryset(self):
        return Comment.objects.filter(product_id=self.kwargs["pk"], is_allowed=True)


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
        category = Category.objects.get(pk=self.kwargs["pk"])
        categories = [category] + category.get_all_subcategories()
        return Product.objects.filter(category__in=categories).prefetch_related("images")


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    context_object_name = "orders"
    template_name = "shop/orders/order_list.html"
    paginate_by = 5

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "shop/orders/order_detail.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_price = 0
        for item in self.object.orderproduct_set.all():
            total_price += item.price_at_purchase * item.quantity

        context["total_price"] = total_price
        return context

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("orderproduct_set")


class OrderCreateView(LoginRequiredMixin, CreateView):
    form_class = OrderForm
    template_name = "shop/orders/order_create.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        cart = Cart(self.request)
        for item in cart:
            OrderProduct.objects.create(
                order=self.object,
                product=item["product"],
                quantity=item["quantity"],
                price_at_purchase=item["price"]
            )
        cart.clear()

        return HttpResponseRedirect(self.get_success_url())


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


def generate_categories(request: HttpRequest, count: int = 10) -> HttpResponse:
    if count < 1:
        return HttpResponse("A number of categories must be greater than zero.", status=HTTPStatus.BAD_REQUEST)

    generate_fake_categories_task.delay(count)
    return HttpResponse("The categories will be created soon.")


def generate_comments(request: HttpRequest, count: int = 10) -> HttpResponse:
    if count < 1:
        return HttpResponse("A number of comments must be greater than zero.", status=HTTPStatus.BAD_REQUEST)

    generate_fake_comments_task.delay(count)
    return HttpResponse("The comments will be created soon.")


def generate_products(request: HttpRequest, count: int = 10) -> HttpResponse:
    if count < 1:
        return HttpResponse("A number of products must be greater than zero.", status=HTTPStatus.BAD_REQUEST)

    generate_fake_products_task.delay(count)
    return HttpResponse("The products will be created soon.")
