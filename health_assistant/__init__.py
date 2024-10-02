from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'health_assistant'

    def ready(self):
        import health_assistant.signals
