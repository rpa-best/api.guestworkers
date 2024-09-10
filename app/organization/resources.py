from import_export import resources
from .models import OrganizationTabel


class OrganizationTabelResource(resources.ModelResource):
    org__name = resources.Field(attribute="org__name", column_name="Организация")
    worker__first_name = resources.Field(attribute="worker__first_name", column_name="Имя")
    worker__last_name = resources.Field(attribute="worker__last_name", column_name="Фамилия")
    date = resources.Field("date", "Дата")
    value = resources.Field("value", "Кол-во часов")

    class Meta:
        model = OrganizationTabel
        fields = ["org__name", "worker__first_name", "worker__last_name", "date", "value"]
