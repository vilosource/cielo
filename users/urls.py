from django.urls import path
from .views import CieloLoginView, CieloLogoutView, CieloPasswordChangeView

app_name = 'users'

urlpatterns = [
    path('login/', CieloLoginView.as_view(), name='login'),
    path('logout/', CieloLogoutView.as_view(), name='logout'),
    path('change-password/', CieloPasswordChangeView.as_view(), name='change_password'),
]
