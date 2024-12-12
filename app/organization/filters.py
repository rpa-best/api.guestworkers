from django_filters import rest_framework as filters
from .models import OrganizationTabel, Document


class OrganizationTabelFilter(filters.FilterSet):
    date_gte = filters.DateFilter("date", "gte")
    date_lte = filters.DateFilter("date", "lte")

    class Meta:
        model = OrganizationTabel
        fields = ["date_gte", "date_lte"]


class DocumentFilter(filters.FilterSet):
    date_gte = filters.DateFilter("date", "gte")
    date_lte = filters.DateFilter("date", "lte")

    class Meta:
        model = Document
        fields = ["date_gte", "date_lte", "type"]
