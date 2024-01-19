from rest_framework import serializers
from .models import Organization, UserToOrganization


class OrganizationShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["inn", "name"]


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


class WorkerToOrganizationSerializer(serializers.ModelSerializer):
    org = OrganizationSerializer()

    class Meta:
        model = UserToOrganization
        exclude = ["user"]
