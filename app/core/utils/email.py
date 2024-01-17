from django.core.mail import send_mail
from django.conf import settings


def send_email(email, subject, message):
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
