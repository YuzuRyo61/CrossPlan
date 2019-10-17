from django.apps import AppConfig


class FediverseConfig(AppConfig):
    name = 'fediverse'

    def ready(self):
        from . import signals
