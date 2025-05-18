from django.apps import AppConfig


class GatePassConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vehicle_pass'

    def ready(self):
        """
        Import and register signals when the application is ready.
        This ensures all signal handlers are connected when Django starts.
        """
        import vehicle_pass.signals  

def ready(self):
    import vehicle_pass.signals

    