from django.apps import AppConfig


class AlertsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alerts'

    def ready(self):
        # Start scheduler when Django starts
        from .scheduler import start_scheduler
        start_scheduler()
