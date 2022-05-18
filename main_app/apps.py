from django.apps import AppConfig
from api_call import *

class MainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_app'

    def ready(self):
        # runFunc()
        pass
