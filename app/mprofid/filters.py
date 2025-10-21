from django_filters import rest_framework as filters
from oauth.models import USER_TYPE_WORKER, USER_TYPES
from .models import WorkerInvoice


class WorkerInvoiceFilter(filters.FilterSet):
    org = filters.CharFilter("worker__usertoorganization__org_id")
    type = filters.ChoiceFilter("worker__type", choices=USER_TYPES)

    class Meta:
        model = WorkerInvoice
        fields = ["org", 'type']

    def __init__(self, data=None, *args, **kwargs):
        data = data.copy() if data is not None else {}
        if "type" not in data:
            data["type"] = USER_TYPE_WORKER
        super().__init__(data, *args, **kwargs)
