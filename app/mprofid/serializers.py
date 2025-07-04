from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .api import Api
from .models import WorkerInvoice


class WorkerInvoiceShowSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = WorkerInvoice
        fields = "__all__"
    
    @extend_schema_field(serializers.JSONField())
    def get_data(self, obj: WorkerInvoice):
        api = Api()
        response = api.get_order(obj.id)
        if not response.ok:
            raise ValidationError(response.json(), 'api_error')
        return response.json()
