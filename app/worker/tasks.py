import datetime
from celery import shared_task
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from oauth.utils import parse_fio, generate_user_email
from organization.models import Organization, UserToOrganization, STATUS_DONE, ROLE_WORKER
from organization.validators import inn_check_api_validator
from .ftp import get_workers
from .models import WorkerDoc, DEFAULT_DOC_TYPES

User = get_user_model()


@shared_task(name=_('Загрузка работников с 1С'))
def update_workers_from_onec():
    fio = 'ФИО'
    passport = 'Серия, номер паспорта'
    inn = 'ИНН подразделения'
    org_name = 'подразделение'
    workers_data = get_workers()
    for row in workers_data:
        worker_fio = row.get(fio, "")
        last_name, first_name, surname = parse_fio(worker_fio)
        worker_passport: str = row.get(passport)
        if not User.objects.filter(passport=worker_passport).exists():
            user = User.objects.create_user(
                email=generate_user_email(),
                first_name=first_name,
                last_name=last_name,
                surname=surname,
                is_staff=True,
                _send_email=False
            )
        else:
            user = User.objects.get(passport=worker_passport)
        for doc in DEFAULT_DOC_TYPES:
            value = row.get(doc["name"])
            WorkerDoc.objects.update_or_create(
                {
                    "user": user,
                    "type_id": doc['slug'],
                    "expired_date": datetime.datetime.strptime(value, "%d.%m.%Y") if value else None
                }, user=user, type_id=doc['slug']
            )
        worker_inn = row.get(inn)
        if not Organization.objects.filter(inn=worker_inn).exists():
            org_data = inn_check_api_validator(worker_inn)
            worker_org = Organization.objects.create(
                inn=worker_inn,
                address = org_data.get('a'),
                name = org_data.get('c') if org_data.get('c') else row.get(org_name, worker_inn),
                ogrn = org_data.get('o'),
                kpp = org_data.get('p'),
            )
        else:
            worker_org = Organization.objects.get(inn=worker_inn)
        UserToOrganization.objects.get_or_create(
            {
                "org": worker_org,
                "user": user,
                "status": STATUS_DONE,
                "role": ROLE_WORKER,
            }, org=worker_org, user=user
        )
