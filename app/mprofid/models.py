from django.core.validators import MinLengthValidator
from django.db import models
from rest_framework.exceptions import ValidationError

from .api import Api


class Service(models.Model):
    """
    {
        "services" : [ // услуги
            {
                "id" : 0, // идентификатор услуги
                "name" : "Оформление личной медицинской книжки", // наименование услуги
            },
            {
                "id" : 0, // идентификатор услуги
                "name" : "Предварительный/периодический медицинский осмотр", // наименование услуги
            }
        ]
    }
    """
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Part(models.Model):
    """
    {
        "parts" : [ // услуги
            {
                "id" : 0, // идентификатор услуги
                "name" : "Фтизиатр", // наименование услуги
            }
        ]
    }
    """
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Med(models.Model):
    """
    {
        "med" : [ // услуги из объёма обследования
            {
                "id" : 0, // идентификатор услуги
                "name" : "Терапевт", // наименование услуги
            },
            {
                "id" : 0, // идентификатор услуги
                "name" : "Клинический анализ крови", // наименование услуги
            }
        ]
    }
    """
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Status(models.Model):
    """
    {
        "status" : [
            {
                "key" : 0, // идентификатор статуса
                "name" : "Создан заказ", // наименование статуса
            },
            {
                "id" : 0, // идентификатор статуса
                "name" : "Проходит обследование", // наименование статуса
            }
        ]
    }
    """
    key = models.SlugField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SurveyType(models.Model):
    """
    {
        "surveyTypes" : [
            {
                "id" : 0, // идентификатор
                "name" : "предварительный", // наименование
            },
            {
                "id" : 0, // идентификатор
                "name" : "периодический", // наименование
            }
        ]
    }
    """
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PayType(models.Model):
    """
    {
        "payTypes" : [
            {
                "id" : 0, // идентификатор
                "name" : "наличный", // наименование
            }
        ]
    }
    """
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Hazard(models.Model):
    """
    {
        "hazards" : [
            {
                "id" : 0, // идентификатор
                "point" : "23.", // пункт
                "name" : "Работы, где имеется контакт с пищевыми продуктами в процессе их производства, хранения, транспортировки и реализации (в организациях пищевых и перерабатывающих отраслей промышленности, сельского хозяйства, пунктах, базах, складах хранения и реализации, в транспортных организациях, организациях торговли, общественного питания, на пищеблоках всех учреждений и организаций)", // наименование
            }
        ]
    }
    """
    id = models.BigIntegerField(primary_key=True)
    point = models.CharField(max_length=255)
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


class ConclusionStatus(models.Model):
    """
    {
        "statuses" : [
            {
                "id" : 1, // идентификатор
                "name" : "Годен", // наименование
            },
            {
                "id" : 2, // идентификатор
                "name" : "Не годен", // наименование
            },
            {
                "id" : 3, // идентификатор
                "name" : "Ограниченно годен", // наименование
            }
        ]
    }
    """
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class MedClient(models.Model):
    """
    {
        "medclients" : [ // услуги
            {
                "id" : 0, // идентификатор договора
                "name" : "ООО Ромашка", // наименование организации
                "altname" : "Ромашка ООО", // наименование организации
                "contractNumber" : "1", // номер договора
                "contractDate" : "2020-01-01" // дата договора
            },
            {
                "id" : 0, // идентификатор договора
                "name" : "ООО Золушка", // наименование организации
                "altname" : "Золушка ООО (ресторан)", // наименование организации
                "contractNumber" : "1", // номер договора
                "contractDate" : "2020-01-01" // дата договора
            }
        ]
    }
    """
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    altname = models.CharField(max_length=255)
    contract_number = models.CharField(max_length=255)
    contract_date = models.DateField()

    def __str__(self):
        return self.name


class Subdivision(models.Model):
    """
    {
        "medclientId" : "0", // договор (id из справочника /medClient)
        "subdivisions" : [ // услуги
            {
                "id" : 0, // идентификатор
                "name" : "Ресторан", // наименование
            },
            {
                "id" : 0, // идентификатор
                "name" : "Склад", // наименование
            }
        ]
    }
    """
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    med_client = models.ForeignKey(MedClient, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Profession(models.Model):
    """
    {
        "medclientId" : "0", // договор (id из справочника /medClient)
        "professions" : [ // услуги
            {
                "id" : 0, // идентификатор
                "name" : "Повар", // наименование
                "hazards" : ["461"]
            },
            {
                "id" : 0, // идентификатор
                "name" : "Официант", // наименование
                "hazards" : []
            }
        ]
    }
    """
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    hazards = models.ManyToManyField(Hazard, blank=True)
    med_client = models.ForeignKey(MedClient, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Order(models.Model):
    """
    POST: {
        "fam": "Иванов Иван Иванович", // ФИО пациента, * required
        "gender": "мужской", // пол пациента (мужской/женский) * required
        "birthday": "1990-01-01", // Дата рождения (yyyy-mm-dd) * required
        "surveyTypeId": "1", // вид осмотра (id из справочника /dictionary/survey)
        "address": "Санкт-Петербург, Лиговский пр, д. 78", // Адрес регистрации
        "citizenship": "Россия", // Гражданство
        "passport": "4000 123411", // Серия и номер паспорта
        "passportDate": "2010-10-11", // Дата выдачи паспорта
        "passportPlace": "ТП №5 УФМС РОССИИ", // Место выдачи
        "phone": "79001234455", // Телефон (11 цифр)
        "snils": "111-111-111 11", // Снилс
        "payType":1, // вид оплаты (id из справочника /dictionary/paytypes) * required
        "medClientId":100, // договор (id из справочника /medClient) * required
        "subdivisionId":1, // подразделение (id из справочника /subdivisions/{medClientId})
        "subdivision":"String", // подразделение, если нет в справочнике /subdivisions/{medClientId}
        "professionId":2, // профессия (id из справочника /professions/{medClientId})
        "profession":"String", // профессия, если нет в справочнике /professions/{medClientId}
        "services": ["5","1"], // оказанные услуги (id из справочника /dictionary/services) * required
        "hazards": ["432", "419"], // Пункты приказа 29н (id из справочника /dictionary/hazards)
        "parts": ["1"] // Доп. услуги (id из справочника /dictionary/parts)
    }
    Response: {
        "id": "55551" // ID направления
    }
    GET: {
        "id" : 0, // идентификатор направления (orderId) в МИС
        "fam" : "Иванов Иван Иванович", // ФИО пациента,
        "gender" : "мужской", // пол пациента
        "birthday" : "01.01.1985", // Дата рождения
        "address": "Санкт-Петербург, Лиговский пр, д. 78", // Адрес регистрации
        "citizenship": "Россия", // Гражданство
        "passport": "4000 123411", // Серия и номер паспорта
        "passportDate": "2010-10-11", // Дата выдачи паспорта
        "passportPlace": "ТП №5 УФМС РОССИИ", // Место выдачи
        "phone": "+7 (900) 000-11-22", // Телефон
        "orderDate" : "15.12.2019", // дата прохождения мед обследования
        "subdivision": {
            "id": "2585", // подразделение (id из справочника /subdivisions/{medClientId})
            "name": "IT" // наименование подразделения
        },
        "profession": {
            "id": "0", // профессия (id из справочника /professions/{medClientId})
            "name": "Повар" // наименование профессии
        },
        "med" : [ // объём обследования пациента
            {
                "id" : 0, // идентификатор услуги
                "name" : "Вакцинация против кори", // наименование услуги
                "date" : "15.12.2019", // дата проведения или результата обследования
            },
            {
                "id" : 0, // идентификатор услуги
                "name" : "ФЛГ", // наименование услуги
                "date" : "15.12.2019", // дата проведения или результата обследования
            }
        ],
        "services" : [ // оказанные услуги
            {
                "id" : 0, // идентификатор группы обследования
                "name" : "Оформление личной медицинской книжки", // наименование услуги
            },
            {
                "id" : 0, // идентификатор группы обследования
                "name" : "Справка 086/у", // наименование услуги
            }
        ],
        "status" : "ready", // Статус направления (key из справочника /dictionary/status)
        "statusName" : "Оформлен", // Наименование статуса
        "startDate" : "2022-01-12 17:14:16", // Начало обследования в медицинском центре
        "finishDate" : "2022-01-12 18:20:18", // Завершение обследования в медицинском центре
        "completeDate" : "2022-01-13 11:35:30", // Готовы итоговые документы
        "deliveryDate" : "2022-01-17 17:10:56" // Передан в доставку,
        "conclusion29n" : [ // Статус заключения по результатам предварительного / периодического осмотра по приказу МЗ РФ № 29н от 28.01.2021 г.
            "id": "1",
            "state": "Годен",
            "text": "Медицинских противопоказаний к работе с указанными вредными и (или) опасными производственными факторами по приказу МЗ РФ № 29н от 28.01.2021 г. не выявлено"
        ]
    }
    """
    id = models.BigIntegerField(primary_key=True)
    fam = models.CharField(max_length=255)
    birthday = models.DateField()
    survey_type = models.ForeignKey(SurveyType, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    citizenship = models.CharField(max_length=255, blank=True, null=True)
    passport = models.CharField(max_length=255, blank=True, null=True)
    passport_date = models.DateField(blank=True, null=True)
    passport_place = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True, validators=[MinLengthValidator(11)])
    snils = models.CharField(max_length=255, blank=True, null=True)
    pay_type = models.ForeignKey(PayType, on_delete=models.CASCADE)
    med_client = models.ForeignKey(MedClient, on_delete=models.CASCADE)
    subdivision = models.ForeignKey(Subdivision, on_delete=models.CASCADE, blank=True, null=True)
    subdivision_other = models.CharField(max_length=255, blank=True, null=True)
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE, blank=True, null=True)
    profession_other = models.CharField(max_length=255, blank=True, null=True)
    services = models.ManyToManyField(Service, blank=True)
    hazards = models.ManyToManyField(Hazard, blank=True)
    parts = models.ManyToManyField(Part, blank=True)
    worker = models.ForeignKey('oauth.User', models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.fam

    @staticmethod
    def get_api_order(order_id):
        api = Api()
        return api.get_order(order_id)

    def get_direction(self):
        api = Api()
        return api.get_direction_order(self.id)

    def delete(self, using=None, keep_parents=False):
        api = Api()
        response = api.delete_order(self.id)
        if not response.ok:
            raise ValidationError(response.text, code='api_error')
        return super(Order, self).delete(using, keep_parents)

    @staticmethod
    def get_api_next_order():
        api = Api()
        return api.get_next_order()