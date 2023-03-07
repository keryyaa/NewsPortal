from django.apps import AppConfig


class PortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portal'

    # Добавляем написанные нами сигналы иначе работать не будут
    def ready(self):
        import portal.signals
