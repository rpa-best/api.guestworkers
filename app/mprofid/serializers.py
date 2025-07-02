from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .api import Api
from .models import Order


@extend_schema_serializer(exclude_fields=['id'])
class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        api = Api()
        response = api.post_order(validated_data)
        if not response.ok:
            raise ValidationError(response.text, 'api_error')
        validated_data['id'] = response.json().get('id')
        return super().create(validated_data)


class OrderShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'fam', 'birthday']

