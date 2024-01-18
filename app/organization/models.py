from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Organization(models.Model):
    name = models.CharField("Название", max_length=255, blank=True)
    inn = models.CharField("ИНН", max_length=20, primary_key=True,
                           validators=[
                               MinLengthValidator(8, 'Неправильный ИНН'),
                               MaxLengthValidator(10, 'Неправильный ИНН'),
                           ])
    bik = models.CharField("ВИК", max_length=255, blank=True)
    address = models.CharField("Адрес", max_length=255, blank=True)
    phone = models.CharField("Телефон", max_length=20, blank=True)
    ogrn = models.CharField("ОГРН", max_length=20, blank=True)
    kpp = models.CharField("КПП", max_length=20, blank=True)

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

    def __str__(self) -> str:
        return self.name

STATUS_CHECKING = 'checking'
STATUS_DONE = 'done'
STATUS_NOTHING = None
STATUS = (
    (STATUS_CHECKING, _('Checking')),
    (STATUS_DONE, _('Done'))
    (STATUS_NOTHING, _('Nothing'))
)

ROLE_OWNER = 'owner'
ROLE_CLIENT = 'client'
ROLE_WORKER = 'worker'
ROLES = (
    (ROLE_OWNER, _('Owner')),
    (ROLE_CLIENT, _('Client')),
    (ROLE_WORKER, _('Worker'))
)

class UserToOrganization(models.Model):
    org = models.ForeignKey(Organization, models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS, null=True)
    role = models.CharField(max_length=20, choices=ROLES, default=ROLE_WORKER)
    
    class Meta:
        unique_together = (("org", "user"),)
    