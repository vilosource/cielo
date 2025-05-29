from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse
import os
import logging

logger = logging.getLogger(__name__)


class CieloLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        logger.debug(f"CieloLoginView.get_success_url called for user: {self.request.user}")
        user = self.request.user
        deployment = os.environ.get('CIELO_DEPLOYMENT', '').lower()
        logger.debug(f"Deployment environment: {deployment}")
        if (
            user.username == 'admin'
            and user.check_password('admin')
            and deployment not in ('development', 'dev')
        ):
            logger.debug("Redirecting admin to change password")
            return reverse('users:change_password')
        success_url = super().get_success_url()
        logger.debug(f"Login success URL: {success_url}")
        return success_url

    def form_valid(self, form):
        logger.debug(f"CieloLoginView.form_valid called for user: {form.get_user()}")
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.debug(f"CieloLoginView.form_invalid called with errors: {form.errors}")
        return super().form_invalid(form)


class CieloPasswordChangeView(PasswordChangeView):
    template_name = 'users/change_password.html'

    def get_success_url(self):
        logger.debug("CieloPasswordChangeView.get_success_url called")
        success_url = reverse('users:login')
        logger.debug(f"Password change success URL: {success_url}")
        return success_url

    def form_valid(self, form):
        logger.debug(f"CieloPasswordChangeView.form_valid called for user: {self.request.user}")
        return super().form_valid(form)


class CieloLogoutView(LogoutView):
    template_name = 'users/logout.html'
    http_method_names = ['get', 'post']  # Allow both GET and POST

    def get_next_page(self):
        """Override to render template instead of redirecting."""
        logger.debug("CieloLogoutView.get_next_page called")
        logger.debug(f"User before logout: {self.request.user}")
        logger.debug(f"User is authenticated: {self.request.user.is_authenticated}")
        return None

    def dispatch(self, request, *args, **kwargs):
        logger.debug(f"CieloLogoutView.dispatch called - Method: {request.method}")
        logger.debug(f"User: {request.user}, Authenticated: {request.user.is_authenticated}")
        logger.debug(f"Session key: {request.session.session_key}")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logger.debug("CieloLogoutView.post called")
        logger.debug(f"User before logout in post: {request.user}")
        response = super().post(request, *args, **kwargs)
        logger.debug(f"Response type: {type(response)}")
        logger.debug(f"Response status: {getattr(response, 'status_code', 'N/A')}")
        return response

    def get(self, request, *args, **kwargs):
        logger.debug("CieloLogoutView.get called")
        logger.debug(f"User in get: {request.user}")
        # For GET requests, actually perform the logout and render the template
        if request.user.is_authenticated:
            logger.debug("User is authenticated, performing logout")
            response = super().post(request, *args, **kwargs)
        else:
            logger.debug("User not authenticated, just render template")
            response = super().get(request, *args, **kwargs)
        logger.debug(f"Response type: {type(response)}")
        return response
