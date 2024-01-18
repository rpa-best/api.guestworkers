from django.apps import AppConfig
from django.db.models.signals import post_migrate
from .management import create_default_doc_types


class WorkerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'worker'

    def ready(self) -> None:
        post_migrate.connect(
            create_default_doc_types,
            dispatch_uid="worker.management.create_default_doc_types",
        )
