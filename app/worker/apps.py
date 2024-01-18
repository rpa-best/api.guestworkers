from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth import apps


class WorkerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'worker'

    def ready(self) -> None:
        post_migrate.connect(
            create_default_doc_types,
            dispatch_uid="django.contrib.auth.management.create_permissions",
        )

        def create_default_doc_types(**kwargs):
            from .models import DocType, DEFAULT_DOC_TYPES

            for doc in DEFAULT_DOC_TYPES:
                DocType.objects.get_or_create(**doc)
