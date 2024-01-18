import datetime
from uuid import uuid4
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, UserManager as _UserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.utils import aware_utcnow
from rest_framework import exceptions
from core.utils.email import send_email
from .utils import generate_password
from .validators import validate_phone


CHANGE_PASSWORD_URL = "https://kk.keyman24.ru/change-password"


class UserManager(_UserManager):

    def _create_user(self, email=None, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save()
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)

    def create_user(self, email=None, password=None, _send_email=True, **extra_fields):
        if not password:
            password = generate_password()
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user: User = self._create_user(email, password, **extra_fields)
        if _send_email:
            user.send_password(password)
        return user


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(_("phone"), blank=True, null=True, validators=[validate_phone], max_length=255)
    surname = models.CharField(_("name"), blank=True, null=True, max_length=255)
    passport = models.CharField(_('passport'), blank=True, null=True, max_length=255, unique=True)
    username = None

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self) -> str:
        name = []
        if self.last_name:
            name.append(self.last_name)
        
        if self.first_name:
            name.append(self.first_name)
        
        if self.surname:
            name.append(self.surname)
        return self.email if not name else " ".join(name)

    def send_password(self, password):
        return send_email(self.email, _("Password"), f"{_('Password')}: {password}")

    def send_reset_password(self):
        uuid = ChangePasswordUUID.create(self.email)
        url = f"{CHANGE_PASSWORD_URL}?uuid={uuid.uuid}"
        return send_email(self.email, _('Reset password'), url)


class ChangePasswordUUID(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    email = models.EmailField(_("email address"))
    expires_at = models.DateTimeField()
    lifetime = datetime.timedelta(minutes=5)

    @classmethod
    def create(cls, email):
        current_time = aware_utcnow()
        expires_at = current_time + cls.lifetime

        return cls.objects.create(
            email=email, expires_at=expires_at,
        )
    
    def validate(self):
        current_time = aware_utcnow()
        if self.expires_at <= current_time - self.lifetime:
            raise exceptions.ValidationError(_("UUID has expired"), "uuid_expired")
        return self
        
    def change_password(self, password):
        user = User.objects.get(email=self.email)
        try:
            validate_password(password)
        except ValidationError as _exp:
            raise exceptions.ValidationError({'password1':  _exp.messages}, getattr(_exp, 'code', None))
        user.password = make_password(password)
        user.save()
        return user
        