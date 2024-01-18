import phonenumbers
from django.core.exceptions import ValidationError


def validate_phone(value: str):
    try:
        phonenumbers.parse(value)
    except Exception:
        raise ValidationError("invalid_phone_number")
    return value
