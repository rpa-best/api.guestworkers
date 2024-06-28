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
from simple_history.models import HistoricalRecords
from core.utils.email import send_email
from organization.models import UserToOrganization, STATUS_CHECKING, ROLE_WORKER, ROLE_CLIENT, ROLE_OWNER
from .utils import generate_password, generate_user_email
from .validators import validate_phone


CHANGE_PASSWORD_URL = "http://95.142.38.166:3050/new-password/"


class UserManager(_UserManager):

    def get_users(self, user, change=False):
        if user.is_anonymous:
            return self.all()
        users_id = []
        exclude_ids = []
        for uto in UserToOrganization.objects.exclude(status=STATUS_CHECKING).filter(user=user):
            if uto.role in [ROLE_WORKER]:
                users_id.append(uto.user_id)
            else:
                users_id = [*users_id, *UserToOrganization.objects.exclude(status=STATUS_CHECKING).filter(org_id=uto.org_id).values_list("user_id", flat=True)]
            if uto.role in [ROLE_CLIENT] and change:
                exclude_ids = [*exclude_ids, *UserToOrganization.objects.exclude(status=STATUS_CHECKING).filter(org_id=uto.org_id, role=ROLE_OWNER).values_list("user_id", flat=True)]
        return self.filter(id__in=users_id).exclude(id__in=exclude_ids)

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
        if not email:
            email = generate_user_email()
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user: User = self._create_user(email, password, **extra_fields)
        if _send_email:
            user.send_password(password)
        return user


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(_("phone"), blank=True, null=True, validators=[validate_phone], max_length=255)
    surname = models.CharField(_("surname"), blank=True, null=True, max_length=255)
    passport = models.CharField(_('passport'), blank=True, null=True, max_length=255, unique=True)
    username = None

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserManager()
    history = HistoricalRecords()

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

    @staticmethod
    def autocomplete_search_fields():
        return ["email", "first_name", "last_name", "surname"]


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
        