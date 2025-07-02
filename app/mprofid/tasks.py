from celery import shared_task
from .api import Api
from .models import *


api = Api()

@shared_task
def sync_mprofid():
    sync_mprofid_dictionaries()
    sync_mprofid_medclients()


@shared_task
def sync_mprofid_dictionaries():
    _sync_services()
    _sync_parts()
    _sync_med()
    _sync_status()
    _sync_survey()
    _sync_paytypes()
    _sync_hazards()
    _sync_conclusion_status()


def _sync_services():
    services = api.get_services().json()

    for service in services.get('services', []):
        try:
            service_obj, created = Service.objects.update_or_create(
                id=service['id'],
                defaults={
                    'name': service['name'],
                }
            )
            print(f"Success syncing service {service_obj}")
        except Exception as e:
            print(f"Error syncing service {service}: {e}")

def _sync_parts():
    parts = api.get_parts().json()

    for part in parts.get('parts', []):
        try:
            part_obj, created = Part.objects.update_or_create(
                id=part['id'],
                defaults={
                    'name': part['name'],
                }
            )
            print(f"Success syncing part {part_obj}")
        except Exception as e:
            print(f"Error syncing part {part}: {e}")


def _sync_med():
    meds = api.get_med().json()

    for med in meds.get('med', []):
        try:
            med_obj, created = Med.objects.update_or_create(
                id=med['id'],
                defaults={
                    'name': med['name'],
                }
            )
            print(f"Success syncing med {med_obj}")
        except Exception as e:
            print(f"Error syncing med {med}: {e}")


def _sync_status():
    statuses = api.get_status().json()

    for status in statuses.get('status', []):
        try:
            status_obj, created = Status.objects.update_or_create(
                key=status['key'],
                defaults={
                    'name': status['name'],
                }
            )
            print(f"Success syncing status {status_obj}")
        except Exception as e:
            print(f"Error syncing status {status}: {e}")


def _sync_survey():
    surveys = api.get_survey().json()

    for survey in surveys.get('surveyTypes', []):
        try:
            survey_obj, created = SurveyType.objects.update_or_create(
                id=survey['id'],
                defaults={
                    'name': survey['name'],
                }
            )
            print(f"Success syncing survey-type {survey_obj}")
        except Exception as e:
            print(f"Error syncing survey-type {survey}: {e}")


def _sync_paytypes():
    paytypes = api.get_paytypes().json()

    for paytype, name in paytypes.get('payTypes', {}).items():
        try:
            paytype_obj, created = PayType.objects.update_or_create(
                id=paytype,
                defaults={
                    'name': name,
                }
            )
            print(f"Success syncing paytype {paytype_obj}")
        except Exception as e:
            print(f"Error syncing paytype {paytype}: {e}")


def _sync_hazards():
    hazards = api.get_hazards().json()

    for hazard in hazards.get('hazards', []):
        try:
            hazard_obj, created = Hazard.objects.update_or_create(
                id=hazard['id'],
                defaults={
                    'point': hazard['point'],
                    'name': hazard['name'],
                }
            )
            print(f"Success syncing hazard {hazard_obj}")
        except Exception as e:
            print(f"Error syncing hazard {hazard}: {e}")

def _sync_conclusion_status():
    conclusion_statuses = api.get_conclusion_status().json()

    for conclusion_status in conclusion_statuses.get('statuses', []):
        try:
            conclusion_status_obj, created = ConclusionStatus.objects.update_or_create(
                id=conclusion_status['id'],
                defaults={
                    'name': conclusion_status['name'],
                }
            )
            print(f"Success syncing conclusion status {conclusion_status_obj}")
        except Exception as e:
            print(f"Error syncing conclusion status {conclusion_status}: {e}")


@shared_task
def sync_mprofid_medclients():
    medclients = api.get_medclients().json()

    for medclient in medclients.get('medclients', []):
        try:
            medclient_obj, created = MedClient.objects.update_or_create(
                id=medclient['id'],
                defaults={
                    'name': medclient['name'],
                    'altname': medclient['altname'],
                    'contract_number': medclient['contractNumber'],
                    'contract_date': medclient['contractDate'],
                }
            )
            print(f"Success syncing medclient {medclient_obj}")
            _sync_subdivisions(medclient_obj.id)
            _sync_professions(medclient_obj.id)
        except Exception as e:
            print(f"Error syncing medclient {medclient}: {e}")


def _sync_subdivisions(med_client_id):
    subdivisions = api.get_subdivisions(med_client_id).json()

    for subdivision in subdivisions.get('subdivisions', []):
        try:
            subdivision_obj, created = Subdivision.objects.update_or_create(
                id=subdivision['id'],
                defaults={
                    'name': subdivision['name'],
                    'med_client_id': med_client_id,
                }
            )
            print(f"Success syncing subdivision {subdivision_obj}")
        except Exception as e:
            print(f"Error syncing subdivision {subdivision}: {e}")


def _sync_professions(med_client_id):
    professions = api.get_professions(med_client_id).json()

    for profession in professions.get('professions', []):
        try:
            profession_obj, created = Profession.objects.update_or_create(
                id=profession['id'],
                defaults={
                    'name': profession['name'],
                    'med_client_id': med_client_id,
                    'hazards': profession['hazards'],
                }
            )
            print(f"Success syncing profession {profession_obj}")
        except Exception as e:
            print(f"Error syncing profession {profession}: {e}")
