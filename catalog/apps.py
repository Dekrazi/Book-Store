from django.apps import AppConfig


class CatalogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "catalog"

    # def ready(self):
    #     from .models import create_custom_permission
    #     create_custom_permission()
