from django.apps import AppConfig


class GatePassConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vehicle_pass'

def ready(self):
    import vehicle_pass.signals