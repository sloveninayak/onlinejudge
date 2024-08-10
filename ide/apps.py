from django.apps import AppConfig

class IdeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ide'
    label = 'ide_unique_label'  # This must be unique
