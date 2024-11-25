from django.views.generic import TemplateView

from shop.models import Product, SliderItem


# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        kwargs.setdefault("view", self)
        kwargs.setdefault("slider_items", SliderItem.objects.all())
        kwargs.setdefault("new_products", Product.objects.all().order_by("-created_at")[:6])
        kwargs.setdefault("sales_products", Product.objects.filter(is_sale=True).order_by("-updated_at")[:6])
        return kwargs


class NotFoundView(TemplateView):
    template_name = "404.html"
