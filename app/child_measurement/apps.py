from django.apps import AppConfig


class ChildMeasurementConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "child_measurement"

    def ready(self):
        import child_measurement.signals
