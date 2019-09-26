from django.apps import AppConfig


class AuthappConfig(AppConfig):
    name = 'AuthApp'
    def ready(self):
        import AuthApp.signals
