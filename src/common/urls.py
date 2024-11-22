from django.urls import path

from common.views import IndexView, NotFoundView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("404/", NotFoundView.as_view(), name="404"),
]
