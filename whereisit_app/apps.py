from django.apps import AppConfig


class WhereisitAppConfig(AppConfig):
    name = 'whereisit_app'

    def ready(self):
        import whereisit_app.signals