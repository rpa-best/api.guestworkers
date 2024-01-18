from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

SOON_EXPIRE_LIMIT = timezone.timedelta(days=5)
UPLOAD_KWARGS = (
    ('first_name', 'Имя', 'Пётр'),
    ('last_name', 'Фамилия', 'Петров'),
    ('surname', 'Отчество', 'Петрович'),
    ('passport', 'Серия, номер паспорта', '99 99 999999'),
)
DEFAULT_DOC_TYPES = [
    {'slug': 'chek_do', 'name': 'Чек до'},
    {'slug': 'polis_oms_do', 'name': 'Полис ОМС до'},
    {'slug': 'polis_dms_do', 'name': 'Полис ДМС до'},
    {'slug': 'projivanie_do', 'name': 'Разрешение на временное проживание до'},
    {'slug': 'jitelstvo_o', 'name': 'Вид на жительство до'},
    {'slug': 'potent_do', 'name': 'патент до'},
]
User = get_user_model()


class DocType(models.Model):
    slug = models.SlugField(primary_key=True)
    name = models.CharField(_('name'), max_length=255, unique=True)
    main = models.BooleanField(default=True)


class WorkerDoc(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    type = models.ForeignKey(DocType, models.SET_NULL, null=True, to_field="slug")
    create_date = models.DateField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    expired_date = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to="user-docs", null=True, blank=True)
    
    @property
    def is_expired(self):
        now = timezone.now().date()
        return self.expired_date < now
    
    @property
    def is_soon_expired(self):
        now = timezone.now()
        date = (now - SOON_EXPIRE_LIMIT).date()
        return self.expired_date <= date
    
    class Meta:
        unique_together = (("type", "user"),)
