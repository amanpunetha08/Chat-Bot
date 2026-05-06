from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = "chatbot.api"

    def ready(self):
        from chatbot.plugins import registry
        registry.autodiscover()
