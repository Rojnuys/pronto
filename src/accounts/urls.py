from django.urls import path, include

from accounts.views import UserLoginView, UserLogoutView, UserRegistrationView, UserActivationView, \
    ConfirmRegistrationView, TokenLifetimeExpiredView

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("registration/", UserRegistrationView.as_view(), name="registration"),
    path("token-lifetime-expired/", TokenLifetimeExpiredView.as_view(), name="token_lifetime_expired"),
    path(
        "activate/<str:uuid64>/<str:token>/",
        UserActivationView.as_view(),
        name="activate_user",
    ),
    path(
        "confirm-registration/",
        ConfirmRegistrationView.as_view(),
        name="confirm_registration",
    ),
    path('oauth/', include('social_django.urls', namespace='social')),
]
