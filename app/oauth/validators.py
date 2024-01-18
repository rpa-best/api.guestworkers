import phonenumbers
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_phone(value: str):
    try:
        phonenumbers.parse(value)
    except Exception:
        raise ValidationError(_("Phone number is invalid"))
    return value
