from celery import shared_task

from .rest import get_contact


@shared_task
def update_contact(contact_id):
    contact = get_contact(contact_id)
    