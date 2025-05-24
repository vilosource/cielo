from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import CieloLoginView, CieloPasswordChangeView

app_name = 'users'

urlpatterns = [
    path('login/', CieloLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', CieloPasswordChangeView.as_view(), name='change_password'),
]
