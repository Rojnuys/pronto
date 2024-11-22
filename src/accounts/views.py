from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, RedirectView, TemplateView

from accounts.forms import UserRegistrationForm
from accounts.services.emails import send_registration_email
from accounts.utils.token_generators import TokenGenerator


# Create your views here.
class UserLoginView(LoginView):
    template_name = "accounts/registration/login.html"


class UserLogoutView(LoginRequiredMixin, LogoutView):
    ...


class UserRegistrationView(CreateView):
    template_name = "accounts/registration/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("confirm_registration")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()

        send_registration_email(self.object, self.request)

        return super().form_valid(form)


class UserActivationView(RedirectView):
    url = reverse_lazy("index")

    def get(self, request, uuid64, token, *args, **kwargs):
        try:
            pk = force_str(urlsafe_base64_decode(uuid64))
            current_user = get_user_model().objects.get(pk=pk)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            return HttpResponseRedirect(reverse_lazy("404"))

        if current_user and TokenGenerator().check_token(current_user, token):
            current_user.is_active = True
            current_user.save()
            login(self.request, current_user, backend="django.contrib.auth.backends.ModelBackend")

            return super().get(self, *args, **kwargs)

        return HttpResponseRedirect(reverse_lazy("token_lifetime_expired"))


class ConfirmRegistrationView(TemplateView):
    template_name = "accounts/registration/confirm_registration.html"


class TokenLifetimeExpiredView(TemplateView):
    template_name = "accounts/registration/token_lifetime_expired.html"
