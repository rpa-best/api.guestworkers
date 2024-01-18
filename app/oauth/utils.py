import secrets
import string

def generate_password(length=8):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))


def generate_user_email():
    from django.contrib.auth import get_user_model

    User = get_user_model()
    last_id = User.objects.all().order_by("id").last().id
    return f'user{last_id + 1}@guestworkers.ru'


def parse_fio(fio: str):
    list_fio = fio.split(" ")
    last_name = list_fio.pop(0).strip()
    try:
        first_name = list_fio.pop(0).strip()
        try:
            surname = " ".join(list_fio).strip()
            return last_name, first_name, surname
        except IndexError:
            return last_name, first_name, None
    except IndexError:
        return last_name, None, None