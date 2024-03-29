import django_filters.rest_framework as filters
from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef, When, Case, Value
from django.utils import timezone
from .models import WorkerDoc, DocType, SOON_EXPIRE_LIMIT, DOC_STATUS_EXPIRED, DOC_STATUS_NORM, DOC_STATUS_SOON_EXPIRED, DOC_STATUS


class WorkerFilter(filters.FilterSet):
    org = filters.CharFilter("usertoorganization__org_id")
    status_doc = filters.ChoiceFilter(choices=DOC_STATUS, method="filter_status_doc")

    class Meta:
        model = get_user_model()
        fields = ["org", "status_doc"]

    def filter_status_doc(self, queryset, name, value):
        now = timezone.now().date()
        return queryset.annotate(
            status_doc=Case(
                When(
                    Exists(
                        WorkerDoc.objects.filter(user_id=OuterRef("id"), expired_date__lte=now)
                    ), Value(DOC_STATUS_EXPIRED)
                ),
                When(
                    Exists(
                        WorkerDoc.objects.filter(user_id=OuterRef("id"), expired_date__lte=now-SOON_EXPIRE_LIMIT)
                    ), Value(DOC_STATUS_SOON_EXPIRED)
                ),
                default=Value(DOC_STATUS_NORM)
            )
        ).filter(status_doc=value)
    

class DocTypeFilter(filters.FilterSet):

    class Meta:
        model = DocType
        fields = ["main"]


class WorkerDocFilter(filters.FilterSet):

    class Meta:
        model = WorkerDoc
        fields = ["type"]