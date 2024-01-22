from django.db import models
from django.conf import settings
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class Organization(models.Model):
    name = models.CharField("Название", max_length=255, blank=True, null=True)
    inn = models.CharField("ИНН", max_length=20, primary_key=True,
                           validators=[
                               MinLengthValidator(8, 'Неправильный ИНН'),
                               MaxLengthValidator(10, 'Неправильный ИНН'),
                           ])
    bik = models.CharField("ВИК", max_length=255, blank=True, null=True)
    address = models.CharField("Адрес", max_length=255, blank=True, null=True)
    phone = models.CharField("Телефон", max_length=20, blank=True, null=True)
    ogrn = models.CharField("ОГРН", max_length=20, blank=True, null=True)
    kpp = models.CharField("КПП", max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_name = models.CharField(max_length=255, blank=True, null=True)
    gen_name = models.CharField(max_length=255, blank=True, null=True)
    r_s = models.CharField(max_length=255, blank=True, null=True)
    k_s = models.CharField(max_length=255, blank=True, null=True)
    has_skud = models.BooleanField(default=False)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

    def __str__(self) -> str:
        return self.name if self.name else self.inn
    
    @classmethod
    def get_orgs(cls, user, change=False):
        if user.is_anonymous:
            return cls.objects.all()
        orgs_id = []
        exclude_ids = []
        for uto in UserToOrganization.objects.exclude(status=STATUS_CHECKING).filter(user=user):
            orgs_id.append(uto.org_id)
            if uto.role in [ROLE_WORKER] and change:
                exclude_ids.append(uto.org_id)
        return cls.objects.filter(id__in=orgs_id).exclude(id__in=exclude_ids)

STATUS_CHECKING = 'checking'
STATUS_DONE = 'done'
STATUS = (
    (STATUS_CHECKING, _('Checking')),
    (STATUS_DONE, _('Done')),
)

ROLE_OWNER = 'owner'
ROLE_CLIENT = 'client'
ROLE_WORKER = 'worker'
ROLES = (
    (ROLE_OWNER, _('Owner')),
    (ROLE_CLIENT, _('Client')),
    (ROLE_WORKER, _('Worker')),
)

class UserToOrganization(models.Model):
    org = models.ForeignKey(Organization, models.CASCADE, verbose_name=_('Организация'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, verbose_name=_('Пользовател'))
    status = models.CharField(max_length=20, choices=STATUS, null=True, verbose_name=_('Статус'))
    role = models.CharField(max_length=20, choices=ROLES, default=ROLE_WORKER, verbose_name=_('Роль'))
    
    class Meta:
        unique_together = (("org", "user"),)
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
    