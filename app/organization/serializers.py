from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, extend_schema_serializer
from .models import Organization, UserToOrganization, ROLE_CLIENT, STATUS_CHECKING, OrganizationDoc, OrganizationTabel, Document, DocumentType


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


@extend_schema_serializer(exclude_fields=["user", "org"])
class OrganizationDocSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationDoc
        fields = "__all__"


@extend_schema_serializer(exclude_fields=["org"])
class OrganizationTabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationTabel
        fields = "__all__"
        read_only_fields = ["editable"]


class DocumentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentType
        fields = "__all__"


class DocumentSerializer(serializers.ModelSerializer):
    type = DocumentTypeSerializer()
    org = OrganizationSerializer()

    class Meta:
        model = Document
        fields = "__all__"
