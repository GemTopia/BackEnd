from django.apps import AppConfig
from .scheduler import start_scheduler


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        start_scheduler()
