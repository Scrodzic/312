from django.apps import AppConfig

class Landing_pageconfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'landing_page'

class PhaseConfig(AppConfig):
    default_auto_field = 'django.db.models.phase'
    name = 'phase'
