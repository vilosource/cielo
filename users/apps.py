from django.apps import AppConfig
import os
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError, ProgrammingError

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        deployment = os.environ.get('CIELO_DEPLOYMENT', '').lower()
        try:
            User = get_user_model()
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        except (OperationalError, ProgrammingError):
            # Database might not be ready during migration commands
            pass
