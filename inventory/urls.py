from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', login_required(views.virtual_machines), name='virtual_machines'),
    path('storage-accounts/', login_required(views.storage_accounts), name='storage_accounts'),
]
