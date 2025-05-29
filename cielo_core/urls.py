from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


def root_redirect(request):
    return redirect('inventory:virtual_machines')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_redirect, name='root'),
    path('users/', include('users.urls')),
    path('inventory/', include('inventory.urls')),
]
