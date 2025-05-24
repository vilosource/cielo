from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse
import os


class CieloLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        user = self.request.user
        deployment = os.environ.get('CIELO_DEPLOYMENT', '').lower()
        if (
            user.username == 'admin'
            and user.check_password('admin')
            and deployment not in ('development', 'dev')
        ):
            return reverse('users:change_password')
        return super().get_success_url()


class CieloPasswordChangeView(PasswordChangeView):
    template_name = 'users/change_password.html'

    def get_success_url(self):
        return reverse('login')
