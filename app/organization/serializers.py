from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import Organization, UserToOrganization, ROLE_CLIENT, STATUS_CHECKING


class OrganizationShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["inn", "name", "ogrn", "address", "kpp"]


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"

    def create(self, validated_data):
        instance: Organization = super().create(validated_data)
        UserToOrganization.objects.create(user=self.context["request"].user, org=instance, status=STATUS_CHECKING, role=ROLE_CLIENT)
        return instance

class OrganizationListSerializer(serializers.ModelSerializer):
    count_workers = serializers.SerializerMethodField()
    class Meta:
        model = Organization
        fields = ["inn", "name", "count_workers"]

    @extend_schema_field(serializers.IntegerField())
    def get_count_workers(self, obj: Organization):
        return UserToOrganization.objects.filter(org=obj).count()


class WorkerToOrganizationSerializer(serializers.ModelSerializer):
    org = OrganizationSerializer()

    class Meta:
        model = UserToOrganization
        exclude = ["user"]


class WorkerToOrganizationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToOrganization
        fields = ["role"]
